# Register urls for the pickups app
from django.urls import path
from .views import place_pickUp_request_Views, pickup_request_views, update_pickup_requests, delete_pickup_request, api_pickup_request_list, api_place_pickup_request, api_update_pickup_request, api_delete_pickup_request

app_name = 'pickups'
urlpatterns = [
    path('pickup-requests/', pickup_request_views, name='display_pickup_requests'),
    path('create-pickup-request/', place_pickUp_request_Views, name='place_pickup_request_views'),
    path('update-pickup-request/<int:pickup_request_id>/', update_pickup_requests, name='update_pickup_requests'),
    path('delete-pickup-request/<int:pickup_request_id>/', delete_pickup_request, name='delete_pickup_requests'),
    # API URLs
    path('api/v1/list/', api_pickup_request_list, name='api_list'),
    path('api/v1/create/', api_place_pickup_request, name='api_create'),
    path('api/v1/update/<int:pickup_request_id>/', api_update_pickup_request, name='api_update'),
    path('api/v1/delete/<int:pickup_request_id>/', api_delete_pickup_request, name='api_delete'),

    ]