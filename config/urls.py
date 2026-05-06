from django.contrib import admin
from django.urls import path, include
from authentication.notifications import notifications_list, mark_read, mark_all_read

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('inventory.urls')),
    path('api/auth/', include('authentication.urls')),
    path('api/notifications/', notifications_list),
    path('api/notifications/<str:notification_id>/read/', mark_read),
    path('api/notifications/read-all/', mark_all_read),
]
