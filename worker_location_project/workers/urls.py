from django.urls import path
from . import views

urlpatterns = [
    path('add-location/', views.add_location, name='add_location'),
    path('add-worker/', views.add_worker, name='add_worker'),
    path('update-worker/<str:worker_id>/', views.update_worker, name='update_worker'),
]
