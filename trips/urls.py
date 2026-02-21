from django.urls import path
from . import views

urlpatterns = [
    path('', views.trip_list, name='trip_list'),
    path('create/', views.trip_create, name='trip_create'),
    path('<int:pk>/', views.trip_detail, name='trip_detail'),
    path('<int:pk>/update/', views.trip_update, name='trip_update'),
    path('<int:pk>/dispatch/', views.trip_dispatch, name='trip_dispatch'),
    path('<int:pk>/complete/', views.trip_complete, name='trip_complete'),
    path('<int:pk>/cancel/', views.trip_cancel, name='trip_cancel'),
]
