# worker_location_project/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from . import consumers
#from workers.consumers import WorkerConsumer  # Replace 'your_app' with your app's name

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(  # Wrap WebSocket with AuthMiddleware for user sessions (optional)
        URLRouter([
            path("ws/workers/", WorkerConsumer.as_asgi()),  # WebSocket route for workers
            path("ws/locations/", WorkerConsumer.as_asgi()),  # Add a similar route for locations (if needed)
        ])
    ),
})
