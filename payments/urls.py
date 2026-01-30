"""
URLs for Payments app
"""
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list, name='list'),
    path('create/', views.payment_create, name='create'),
    path('<int:pk>/', views.payment_detail, name='detail'),
    path('<int:pk>/update/', views.payment_update, name='update'),
    path('<int:pk>/delete/', views.payment_delete, name='delete'),
]

