from django.urls import path
from . import views

urlpatterns = [
    path('', views.maintenance_list, name='maintenance_list'),
    path('create/', views.maintenance_create, name='maintenance_create'),
    path('<int:pk>/update/', views.maintenance_update, name='maintenance_update'),
    path('fuel/', views.fuel_list, name='fuel_list'),
    path('fuel/create/', views.fuel_create, name='fuel_create'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/create/', views.expense_create, name='expense_create'),
]
