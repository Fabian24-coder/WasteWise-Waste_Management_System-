# Register urls for the pickups app
from django.urls import path
from .views import createpickUp_request_Views, pickup_request_views


urlpatterns = [
    path('pickup-requests/', pickup_request_views, name='pickup_request_views'),
    path('create-pickup-request/', createpickUp_request_Views, name='create_pickup_request_views')
]