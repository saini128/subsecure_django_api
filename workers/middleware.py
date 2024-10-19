import jwt
from channels.middleware import BaseMiddleware
from channels.exceptions import DenyConnection
from django.conf import settings
from channels.auth import get_user

class WebSocketJWTAuthMiddleware(BaseMiddleware):
    """
    Middleware to handle JWT authentication for WebSocket connections.
    """

    async def __call__(self, scope, receive, send):
        # Extract the JWT token from the WebSocket headers
        token = self.get_token_from_headers(scope)

        if token:
            # Verify and decode the JWT token
            try:
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get('user_id')

                # Set the user in the scope
                scope['user'] = await get_user(user_id)  # This method should be implemented to retrieve user

            except jwt.ExpiredSignatureError:
                # Token has expired
                raise DenyConnection("JWT token has expired.")
            except jwt.InvalidTokenError:
                # Token is invalid
                raise DenyConnection("Invalid JWT token.")
        
        return await super().__call__(scope, receive, send)

    def get_token_from_headers(self, scope):
        """
        Extracts the JWT token from the WebSocket headers.
        """
        # Extract the headers
        headers = dict(scope['headers'])
        # The token is expected to be in the format: "Authorization: Bearer <token>"
        if b'authorization' in headers:
            auth_header = headers[b'authorization'].decode('utf-8')
            # Check if the token starts with "Bearer"
            if auth_header.startswith('Bearer '):
                return auth_header.split(' ')[1]  # Return the token part
        return None
