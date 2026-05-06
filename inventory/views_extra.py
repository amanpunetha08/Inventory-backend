from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from .db import db

orders_collection = db['orders']
suppliers_collection = db['suppliers']
categories_collection = db['categories']


def serialize(doc):
    doc['id'] = str(doc.pop('_id'))
    return doc


# --- ORDERS ---
@api_view(['GET', 'POST'])
def orders_list(request):
    if request.method == 'GET':
        orders = list(orders_collection.find({'user': request.user.username}).sort('created_at', -1))
        return Response([serialize(o) for o in orders])
    data = request.data.copy()
    data['user'] = request.user.username
    data['status'] = data.get('status', 'Pending')
    data['created_at'] = datetime.utcnow()
    result = orders_collection.insert_one(data)
    data['id'] = str(result.inserted_id)
    data.pop('_id', None)
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, order_id):
    try:
        oid = ObjectId(order_id)
    except Exception:
        return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
    doc = orders_collection.find_one({'_id': oid, 'user': request.user.username})
    if not doc:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return Response(serialize(doc))
    if request.method == 'PUT':
        data = request.data.copy()
        data.pop('id', None)
        data.pop('user', None)
        orders_collection.update_one({'_id': oid}, {'$set': data})
        return Response(serialize(orders_collection.find_one({'_id': oid})))
    orders_collection.delete_one({'_id': oid})
    return Response(status=status.HTTP_204_NO_CONTENT)


# --- SUPPLIERS ---
@api_view(['GET', 'POST'])
def suppliers_list(request):
    if request.method == 'GET':
        suppliers = list(suppliers_collection.find({'user': request.user.username}).sort('created_at', -1))
        return Response([serialize(s) for s in suppliers])
    data = request.data.copy()
    data['user'] = request.user.username
    data['created_at'] = datetime.utcnow()
    result = suppliers_collection.insert_one(data)
    data['id'] = str(result.inserted_id)
    data.pop('_id', None)
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def supplier_detail(request, supplier_id):
    try:
        oid = ObjectId(supplier_id)
    except Exception:
        return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
    doc = suppliers_collection.find_one({'_id': oid, 'user': request.user.username})
    if not doc:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return Response(serialize(doc))
    if request.method == 'PUT':
        data = request.data.copy()
        data.pop('id', None)
        data.pop('user', None)
        suppliers_collection.update_one({'_id': oid}, {'$set': data})
        return Response(serialize(suppliers_collection.find_one({'_id': oid})))
    suppliers_collection.delete_one({'_id': oid})
    return Response(status=status.HTTP_204_NO_CONTENT)


# --- CATEGORIES ---
@api_view(['GET', 'POST'])
def categories_list(request):
    if request.method == 'GET':
        cats = list(categories_collection.find({'user': request.user.username}).sort('name', 1))
        return Response([serialize(c) for c in cats])
    data = request.data.copy()
    data['user'] = request.user.username
    data['created_at'] = datetime.utcnow()
    result = categories_collection.insert_one(data)
    data['id'] = str(result.inserted_id)
    data.pop('_id', None)
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, category_id):
    try:
        oid = ObjectId(category_id)
    except Exception:
        return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
    doc = categories_collection.find_one({'_id': oid, 'user': request.user.username})
    if not doc:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return Response(serialize(doc))
    if request.method == 'PUT':
        data = request.data.copy()
        data.pop('id', None)
        data.pop('user', None)
        categories_collection.update_one({'_id': oid}, {'$set': data})
        return Response(serialize(categories_collection.find_one({'_id': oid})))
    categories_collection.delete_one({'_id': oid})
    return Response(status=status.HTTP_204_NO_CONTENT)
