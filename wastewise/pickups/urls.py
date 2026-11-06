# Register urls for the pickups app
from django.urls import path
from .views import (
    api_confirm_collection,
    api_confirm_payment,
    api_decide_pickup_request,
    api_delete_pickup_request,
    api_pickup_request_list,
    api_place_pickup_request,
    api_update_pickup_request,
    api_waste_rates,
    confirm_payment,
    confirm_pickup_collection,
    delete_pickup_request,
    pickup_request_views,
    place_pickUp_request_Views,
    pickup_dashboard,
    update_pickup_requests,
)

app_name = 'pickups'
urlpatterns = [
    path('dashboard/', pickup_dashboard, name='dashboard'),
    path('pickup-requests/', pickup_request_views, name='display_pickup_requests'),
    path('create-pickup-request/', place_pickUp_request_Views, name='place_pickup_request_views'),
    path('update-pickup-request/<int:pickup_request_id>/', update_pickup_requests, name='update_pickup_requests'),
    path('pickup-request/<int:pickup_request_id>/payment/', confirm_payment, name='confirm_payment'),
    path('pickup-request/<int:pickup_request_id>/confirm-collection/', confirm_pickup_collection, name='confirm_collection'),
    path('delete-pickup-request/<int:pickup_request_id>/', delete_pickup_request, name='delete_pickup_requests'),
    # API URLs
    path('api/v1/list/', api_pickup_request_list, name='api_list'),
    path('api/v1/create/', api_place_pickup_request, name='api_create'),
    path('api/v1/waste-rates/', api_waste_rates, name='api_waste_rates'),
    path('api/v1/<int:pickup_request_id>/decision/', api_decide_pickup_request, name='api_decision'),
    path('api/v1/<int:pickup_request_id>/payment/', api_confirm_payment, name='api_payment'),
    path('api/v1/<int:pickup_request_id>/confirm-collection/', api_confirm_collection, name='api_confirm_collection'),
    path('api/v1/update/<int:pickup_request_id>/', api_update_pickup_request, name='api_update'),
    path('api/v1/delete/<int:pickup_request_id>/', api_delete_pickup_request, name='api_delete'),

    ]