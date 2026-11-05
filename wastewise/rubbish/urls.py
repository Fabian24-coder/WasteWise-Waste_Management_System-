from django.urls import path
from . import views

urlpatterns = [
    path('', views.rubbish_list, name='rubbish_list'),
    path('add/', views.rubbish_create, name='rubbish_create'),
    path('<int:pk>/edit/', views.rubbish_update, name='rubbish_update'),
    path('<int:pk>/toggle/', views.rubbish_toggle, name='rubbish_toggle'),
]
