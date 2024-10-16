import os

from workers.middleware import WebSocketJWTAuthMiddleware  # This handles JWT-based authentication for WebSockets
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from workers import routing  # Import your WebSocket routing (this should contain your WebSocket URL patterns)

# Set the settings module to your project's settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worker_location_project.settings")

# Define the application protocol router for handling different types of connections (HTTP and WebSocket)
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),  # Handle traditional HTTP requests
        "websocket": WebSocketJWTAuthMiddleware(  # Handle WebSocket connections with JWT auth middleware
            URLRouter(routing.websocket_urlpatterns)  # Use URLRouter to handle WebSocket URL patterns
        ),
    }
)