"""
ASGI config for worker_location_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# worker_location_project/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from workers.consumers import WorkerConsumer  # Import your WebSocket consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worker_location_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handle traditional HTTP requests
    "websocket": AuthMiddlewareStack(  # Handle WebSocket connections
        URLRouter([
            path("ws/workers/", WorkerConsumer.as_asgi()),  # Define WebSocket endpoint for workers
            path("ws/locations/", WorkerConsumer.as_asgi()),  # Optional: WebSocket endpoint for locations
        ])
    ),
})

#application = get_asgi_application()