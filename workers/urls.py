from django.urls import path
from . import views

urlpatterns = [
    path('get-all-locations/', views.get_all_locations, name='get_all_locations'), #GET
    path('get-all-workers/', views.get_all_workers, name='get_all_workers'), #GET
    path('add-location/', views.add_location, name='add_location'), #POST
    path('add-worker/', views.add_worker, name='add_worker'), #POST
    path('update-workers/', views.update_workers, name='update_workers'), #PUT
    path('update-worker/<str:worker_id>/', views.update_worker, name='update_worker'), #PUT
    path('delete-worker/<str:worker_id>/', views.delete_worker, name='delete_worker'), #DELETE
    path('delete-location/<str:location_id>/', views.delete_location, name='delete_location'), #DELETE
    path('api/workers/', views.worker_list, name='worker_list'), #GET, POST
    path('api/locations/', views.location_list, name='location_list'), #GET, POST
    path('end-shift/', views.end_shift, name='end_shift'), #GET
]
