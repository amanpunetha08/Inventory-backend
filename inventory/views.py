from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from .db import db
from authentication.notifications import create_notification

items_collection = db['items']

REQUIRED_FIELDS = ['name', 'quantity', 'price']


def serialize_item(item):
    item['id'] = str(item.pop('_id'))
    item.setdefault('sku', '')
    item.setdefault('category', '')
    item.setdefault('description', '')
    item['quantity'] = int(item.get('quantity', 0))
    item['price'] = float(item.get('price', 0))
    return item


@api_view(['GET', 'POST'])
def items_list(request):
    if request.method == 'GET':
        query = {'user': request.user.username}
        search = request.query_params.get('search', '').strip()
        if search:
            query['$or'] = [
                {'name': {'$regex': search, '$options': 'i'}},
                {'sku': {'$regex': search, '$options': 'i'}},
                {'category': {'$regex': search, '$options': 'i'}},
            ]
        category = request.query_params.get('category', '').strip()
        if category:
            query['category'] = category
        status = request.query_params.get('status', '').strip()
        if status == 'in_stock':
            query['quantity'] = {'$gt': 5}
        elif status == 'low_stock':
            query['quantity'] = {'$gt': 0, '$lte': 5}
        elif status == 'out_of_stock':
            query['quantity'] = 0
        min_price = request.query_params.get('min_price', '').strip()
        max_price = request.query_params.get('max_price', '').strip()
        if min_price or max_price:
            price_q = {}
            if min_price:
                price_q['$gte'] = float(min_price)
            if max_price:
                price_q['$lte'] = float(max_price)
            query['price'] = price_q
        sort_by = request.query_params.get('sort', '').strip()
        sort_field = 'created_at'
        sort_dir = -1
        if sort_by == 'name_asc':
            sort_field, sort_dir = 'name', 1
        elif sort_by == 'name_desc':
            sort_field, sort_dir = 'name', -1
        elif sort_by == 'price_asc':
            sort_field, sort_dir = 'price', 1
        elif sort_by == 'price_desc':
            sort_field, sort_dir = 'price', -1
        elif sort_by == 'quantity_asc':
            sort_field, sort_dir = 'quantity', 1
        elif sort_by == 'quantity_desc':
            sort_field, sort_dir = 'quantity', -1
        items = list(items_collection.find(query).sort(sort_field, sort_dir))
        return Response([serialize_item(i) for i in items])

    data = request.data.copy()
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] in [None, '']:
            return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

    data['user'] = request.user.username
    data['quantity'] = int(data.get('quantity', 0))
    data['price'] = float(data.get('price', 0))
    data['created_at'] = datetime.utcnow()
    data['updated_at'] = datetime.utcnow()
    result = items_collection.insert_one(data)
    data['id'] = str(result.inserted_id)
    data.pop('_id', None)

    if data['quantity'] == 0:
        create_notification(request.user.username, f"{data['name']} is out of stock", 'alert')
    elif data['quantity'] <= 5:
        create_notification(request.user.username, f"{data['name']} is low on stock ({data['quantity']} left)", 'warning')

    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def items_stats(request):
    user_query = {'user': request.user.username}
    all_items = list(items_collection.find(user_query))

    total = len(all_items)
    low_stock = sum(1 for i in all_items if 0 < int(i.get('quantity', 0)) <= 5)
    out_of_stock = sum(1 for i in all_items if int(i.get('quantity', 0)) == 0)
    total_value = sum(float(i.get('price', 0)) * int(i.get('quantity', 0)) for i in all_items)

    # Calculate changes vs last month
    last_month = datetime.utcnow() - timedelta(days=30)
    old_items = [i for i in all_items if i.get('created_at', datetime.utcnow()) < last_month]
    old_total = len(old_items) if old_items else max(total - 1, 1)

    return Response({
        'total_products': total,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'total_value': round(total_value, 2),
        'changes': {
            'total_products': round(((total - old_total) / max(old_total, 1)) * 100, 1),
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
            'total_value': round(total_value, 2),
        }
    })


@api_view(['GET', 'PUT', 'DELETE'])
def item_detail(request, item_id):
    try:
        oid = ObjectId(item_id)
    except Exception:
        return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)

    item = items_collection.find_one({'_id': oid, 'user': request.user.username})
    if not item:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(serialize_item(item))

    if request.method == 'PUT':
        data = request.data.copy()
        data.pop('id', None)
        data.pop('user', None)
        if 'quantity' in data:
            data['quantity'] = int(data['quantity'])
        if 'price' in data:
            data['price'] = float(data['price'])
        data['updated_at'] = datetime.utcnow()
        items_collection.update_one({'_id': oid}, {'$set': data})
        updated = items_collection.find_one({'_id': oid})

        qty = int(updated.get('quantity', 0))
        name = updated.get('name', '')
        if qty == 0:
            create_notification(request.user.username, f"{name} is now out of stock", 'alert')
        elif qty <= 5:
            create_notification(request.user.username, f"{name} stock is low ({qty} left)", 'warning')

        return Response(serialize_item(updated))

    if request.method == 'DELETE':
        items_collection.delete_one({'_id': oid})
        return Response(status=status.HTTP_204_NO_CONTENT)
