# workers/routing.py
from django.urls import path
from .consumers import WorkerConsumer, LocationConsumer

websocket_urlpatterns = [
    path('ws/workers/', WorkerConsumer.as_asgi()),
    path('ws/locations/', LocationConsumer.as_asgi()),
]
