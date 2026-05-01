from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.billing_settings, name='billing_settings'),
    path('generate/', views.generate_bills, name='generate_bills'),
    path('', views.bill_list, name='bill_list'),
    path('<int:pk>/edit/', views.bill_edit, name='bill_edit'),
    path('<int:pk>/payment/', views.bill_payment, name='bill_payment'),
    path('<int:pk>/receipt/', views.bill_receipt, name='bill_receipt'),
    path('<int:pk>/delete/', views.bill_delete, name='bill_delete'),
]
