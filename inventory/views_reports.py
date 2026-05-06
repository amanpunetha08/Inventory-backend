from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from inventory.db import db


@api_view(['GET'])
def reports(request):
    user = request.user.username
    items = list(db['items'].find({'user': user}))
    orders = list(db['orders'].find({'user': user}))

    # Inventory summary
    total_items = len(items)
    total_quantity = sum(int(i.get('quantity', 0)) for i in items)
    total_value = sum(float(i.get('price', 0)) * int(i.get('quantity', 0)) for i in items)
    avg_price = total_value / total_quantity if total_quantity else 0

    # Category report
    category_report = {}
    for i in items:
        cat = i.get('category', 'Uncategorized')
        if cat not in category_report:
            category_report[cat] = {'items': 0, 'quantity': 0, 'value': 0}
        category_report[cat]['items'] += 1
        category_report[cat]['quantity'] += int(i.get('quantity', 0))
        category_report[cat]['value'] += float(i.get('price', 0)) * int(i.get('quantity', 0))

    # Stock distribution
    in_stock = sum(1 for i in items if int(i.get('quantity', 0)) > 5)
    low_stock = sum(1 for i in items if 0 < int(i.get('quantity', 0)) <= 5)
    out_of_stock = sum(1 for i in items if int(i.get('quantity', 0)) == 0)

    # Top items by value
    top_by_value = sorted(items, key=lambda i: float(i.get('price', 0)) * int(i.get('quantity', 0)), reverse=True)[:5]
    top_items = [{'name': i['name'], 'value': float(i.get('price', 0)) * int(i.get('quantity', 0)), 'quantity': int(i.get('quantity', 0))} for i in top_by_value]

    # Orders summary
    total_orders = len(orders)
    total_order_value = sum(float(o.get('total', 0)) for o in orders)
    orders_by_status = {}
    for o in orders:
        s = o.get('status', 'Unknown')
        orders_by_status[s] = orders_by_status.get(s, 0) + 1

    return Response({
        'inventory': {
            'total_items': total_items,
            'total_quantity': total_quantity,
            'total_value': round(total_value, 2),
            'avg_price': round(avg_price, 2),
        },
        'stock_distribution': {
            'in_stock': in_stock,
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
        },
        'category_report': category_report,
        'top_items': top_items,
        'orders': {
            'total_orders': total_orders,
            'total_value': round(total_order_value, 2),
            'by_status': orders_by_status,
        },
    })


@api_view(['GET'])
def alerts(request):
    user = request.user.username
    items = list(db['items'].find({'user': user}))

    alerts_list = []

    # Out of stock alerts
    for i in items:
        qty = int(i.get('quantity', 0))
        if qty == 0:
            alerts_list.append({'type': 'critical', 'title': 'Out of Stock', 'message': f"{i['name']} ({i.get('sku', '')}) has no stock", 'item': i['name']})
        elif qty <= 5:
            alerts_list.append({'type': 'warning', 'title': 'Low Stock', 'message': f"{i['name']} ({i.get('sku', '')}) only {qty} left", 'item': i['name']})

    # Pending orders alert
    pending = list(db['orders'].find({'user': user, 'status': 'Pending'}))
    for o in pending:
        alerts_list.append({'type': 'info', 'title': 'Pending Order', 'message': f"Order for {o.get('product', '')} from {o.get('supplier', '')} is pending", 'item': o.get('product', '')})

    return Response({
        'alerts': alerts_list,
        'summary': {
            'critical': sum(1 for a in alerts_list if a['type'] == 'critical'),
            'warning': sum(1 for a in alerts_list if a['type'] == 'warning'),
            'info': sum(1 for a in alerts_list if a['type'] == 'info'),
        }
    })
