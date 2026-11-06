from django.urls import path
from . import views

app_name = "collectors"

urlpatterns = [
    # api 
    path('api/zones/', views.api_display_zones, name='api_display_zones'),
    path('api/zones/create/', views.api_zone_create, name='api_zone_create'),
    path('api/zones/<int:pk>/', views.api_zone_get, name='api_zone_get'),
    path('api/zones/<int:pk>/update/', views.api_zone_update, name='api_zone_update'),
    path('api/zones/<int:pk>/delete/', views.api_zone_delete, name='api_zone_delete'),

    path('api/collectors/', views.api_display_collectors, name='api_display_collectors'),
    path('api/collectors/create/', views.api_collector_create, name='api_collector_create'),
    path('api/collectors/<int:pk>/', views.api_collector_get, name='api_collector_get'),
    path('api/collectors/<int:pk>/update/', views.api_collector_update, name='api_collector_update'),
    path('api/collectors/<int:pk>/delete/', views.api_collector_delete, name='api_collector_delete'),

    # pages 
    path('collectors/zones/', views.display_zones, name='display_zones'),
    path('collectors/zones/<int:zone_id>/update/', views.update_zone, name='update_zone'),
    path('collectors/zones/<int:zone_id>/delete/', views.delete_zone, name='delete_zone'),

    path('collectors/', views.display_collectors, name='display_collectors'),
    path('collectors/<int:collector_id>/update/', views.update_collector, name='update_collector'),
    path('collectors/<int:collector_id>/delete/', views.delete_collector, name='delete_collector'),
]