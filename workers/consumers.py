# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.contrib.auth.models import AnonymousUser

# class WorkerConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Accept the WebSocket connection
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Handle WebSocket disconnection
#         pass

#     async def receive(self, text_data):
#         # Handle data received from WebSocket
#         workers = await self.get_all_workers()
#         # Send the worker data back to the client as JSON
#         await self.send(text_data=json.dumps(workers))

#     async def get_all_workers(self):
#         # Logic to get all workers from the database
#         from .models import Workers  # Import the Workers model
#         workers = list(Workers.objects.values())  # Convert queryset to a list of dictionaries
#         return workers


# # class LocationConsumer(AsyncWebsocketConsumer):
# #     async def connect(self):
# #         # Accept the WebSocket connection
# #         await self.accept()

# #     async def disconnect(self, close_code):
# #         # Handle WebSocket disconnection
# #         pass

# #     async def receive(self, text_data):
# #         # Handle data received from WebSocket
# #         locations = await self.get_all_locations()
# #         # Send the location data back to the client as JSON
# #         await self.send(text_data=json.dumps(locations))

# #     async def get_all_locations(self):
# #         # Logic to get all locations from the database
# #         from .models import Location  # Import the Location model
# #         locations = list(Location.objects.values())  # Convert queryset to a list of dictionaries
# #         return locations

# workers/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WorkerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        # For now, echo the message back
        await self.send(text_data=json.dumps({
            'message': data.get('message', 'No message received')
        }))
