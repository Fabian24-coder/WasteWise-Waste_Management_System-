# Register urls for the pickups app
from django.urls import path
from .views import pickup_request_views


urlpatterns = [
    path('pickup-requests/', pickup_request_views, name='pickup_request_views'),
]