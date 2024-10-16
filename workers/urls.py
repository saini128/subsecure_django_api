from django.urls import path
from . import views

urlpatterns = [
    path('get-all-locations/', views.get_all_locations, name='get_all_locations'),
    path('get-all-workers/', views.get_all_workers, name='get_all_workers'),
    path('add-location/', views.add_location, name='add_location'),
    path('add-worker/', views.add_worker, name='add_worker'),
    path('update-worker/<str:worker_id>/', views.update_worker, name='update_worker'),
    path('delete-worker/<str:worker_id>/', views.delete_worker, name='delete_worker'),
    path('delete-location/<str:location_id>/', views.delete_location, name='delete_location'),
    path('api/workers/', views.worker_list, name='worker_list'),
    path('api/locations/', views.location_list, name='location_list'),
]
