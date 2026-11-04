from django.urls import path
from . import views

urlpatterns = [
    # zones
    path('zones/', views.display_zones, name='display_zones'),
    path('zones/create/', views.zone_create, name='zone_create'),
    path('zones/<int:pk>/', views.zone_get, name='zone_get'),
    path('zones/<int:pk>/update/', views.zone_update, name='zone_update'),
    path('zones/<int:pk>/delete/', views.zone_delete, name='zone_delete'),

    # collectors
    path('collectors/', views.display_collectors, name='display_collectors'),
    path('collectors/create/', views.collector_create, name='collector_create'),
    path('collectors/<int:pk>/', views.collector_get, name='display_collector'),
    path('collectors/<int:pk>/update/', views.collector_update, name='update_collector'),
    path('collectors/<int:pk>/delete/', views.collector_delete, name='delete_collector'),
]