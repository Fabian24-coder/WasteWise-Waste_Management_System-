from django.urls import path
from . import views

urlpatterns = [
    # api
    path('api/payments/', views.display_payments, name='display_payments'),
    path('api/payments/create/', views.payment_create, name='payment_create'),
    path('api/payments/<int:pk>/', views.payment_get, name='payment_get'),
    path('api/payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),

    # pages
    path('payments/', views.payments_page, name='payments_page'),
]