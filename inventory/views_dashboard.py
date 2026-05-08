from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from inventory.db import db


@api_view(['GET'])
def dashboard(request):
    user = request.user.username
    items = list(db['items'].find({'user': user}))
    orders = list(db['orders'].find({'user': user}))
    suppliers = list(db['suppliers'].find({'user': user}))
    categories = list(db['categories'].find({'user': user}))
    warehouses = list(db['warehouses'].find({'user': user}))

    total_products = len(items)
    total_stock = sum(int(i.get('quantity', 0)) for i in items)
    low_stock = sum(1 for i in items if 0 < int(i.get('quantity', 0)) <= 5)
    out_of_stock = sum(1 for i in items if int(i.get('quantity', 0)) == 0)
    total_value = sum(float(i.get('price', 0)) * int(i.get('quantity', 0)) for i in items)

    total_orders = len(orders)
    pending_orders = sum(1 for o in orders if o.get('status') == 'Pending')
    shipped_orders = sum(1 for o in orders if o.get('status') == 'Shipped')
    delivered_orders = sum(1 for o in orders if o.get('status') == 'Delivered')

    # Category breakdown
    category_stats = {}
    for i in items:
        cat = i.get('category', 'Uncategorized')
        if cat not in category_stats:
            category_stats[cat] = {'count': 0, 'value': 0}
        category_stats[cat]['count'] += 1
        category_stats[cat]['value'] += float(i.get('price', 0)) * int(i.get('quantity', 0))

    # Recent orders
    recent_orders = sorted(orders, key=lambda o: o.get('created_at', datetime.min), reverse=True)[:5]
    for o in recent_orders:
        o['id'] = str(o.pop('_id'))

    # Low stock items
    low_stock_items = [{'name': i['name'], 'quantity': i['quantity'], 'sku': i.get('sku', '')} for i in items if 0 < int(i.get('quantity', 0)) <= 5]

    # Warehouse summary
    warehouse_summary = []
    for w in warehouses:
        warehouse_summary.append({
            'id': str(w['_id']),
            'name': w.get('name', ''),
            'location': w.get('location', ''),
            'stock': int(w.get('stock', 0)),
        })

    return Response({
        'summary': {
            'total_products': total_products,
            'total_stock': total_stock,
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
            'total_value': round(total_value, 2),
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'total_suppliers': len(suppliers),
            'total_categories': len(categories),
            'total_warehouses': len(warehouses),
        },
        'orders_breakdown': {
            'pending': pending_orders,
            'shipped': shipped_orders,
            'delivered': delivered_orders,
        },
        'category_stats': category_stats,
        'recent_orders': recent_orders,
        'low_stock_items': low_stock_items,
        'warehouse_summary': warehouse_summary,
    })
