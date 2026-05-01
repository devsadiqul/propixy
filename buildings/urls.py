from django.urls import path
from . import views

urlpatterns = [
    # Buildings
    path('', views.building_list, name='building_list'),
    path('create/', views.building_create, name='building_create'),
    path('<int:pk>/edit/', views.building_edit, name='building_edit'),
    path('<int:pk>/delete/', views.building_delete, name='building_delete'),
    
    # Units
    path('units/', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/<int:pk>/edit/', views.unit_edit, name='unit_edit'),
    path('units/<int:pk>/delete/', views.unit_delete, name='unit_delete'),
]
