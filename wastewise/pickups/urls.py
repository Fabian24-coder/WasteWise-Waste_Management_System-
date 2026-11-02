# Register urls for the pickups app
from django.urls import path
from .views import createpickUp_request_Views, pickup_request_views, update_pickup_requests, delete_pickup_request


urlpatterns = [
    path('pickup-requests/', pickup_request_views, name='pickup_request_views'),
    path('create-pickup-request/', createpickUp_request_Views, name='create_pickup_request_views'),
    path('update-pickup-request/<int:pickup_request_id>/', update_pickup_requests, name='update_pickup_requests'),
    path('delete-pickup-request/<int:pickup_request_id>/', delete_pickup_request, name='delete_pickup_requests'),
    ]