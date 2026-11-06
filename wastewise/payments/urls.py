from django.urls import path
from . import views

urlpatterns = [
    path('payments/', views.display_payments, name='display_payments'),
    path('payments/create/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/', views.payment_get, name='payment_get'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),
]