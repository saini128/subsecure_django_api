# workers/routing.py
from django.urls import re_path
from .consumers import WorkerConsumer, LocationConsumer

websocket_urlpatterns = [
    re_path('ws/workers/', WorkerConsumer.as_asgi()),
    re_path('ws/locations/', LocationConsumer.as_asgi()),
]
