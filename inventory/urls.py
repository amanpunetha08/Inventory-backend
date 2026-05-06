from django.urls import path
from .views import items_list, item_detail, items_stats
from .views_extra import orders_list, order_detail, suppliers_list, supplier_detail, categories_list, category_detail
from .views_dashboard import dashboard
from .views_currency import exchange_rates
from .views_reports import reports, alerts

urlpatterns = [
    path('items/', items_list),
    path('items/stats/', items_stats),
    path('items/<str:item_id>/', item_detail),
    path('orders/', orders_list),
    path('orders/<str:order_id>/', order_detail),
    path('suppliers/', suppliers_list),
    path('suppliers/<str:supplier_id>/', supplier_detail),
    path('categories/', categories_list),
    path('categories/<str:category_id>/', category_detail),
    path('dashboard/', dashboard),
    path('exchange-rates/', exchange_rates),
    path('reports/', reports),
    path('alerts/', alerts),
]
