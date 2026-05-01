from django.urls import path
from . import views

urlpatterns = [
    path('', views.tenant_list, name='tenant_list'),
    path('create/', views.tenant_create, name='tenant_create'),
    path('<int:pk>/edit/', views.tenant_edit, name='tenant_edit'),
    path('<int:pk>/delete/', views.tenant_delete, name='tenant_delete'),
]
