# workers/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Worker, Location

class WorkerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        workers = Worker.objects.all().values('name', 'age', 'location__location_description')
        await self.send(text_data=json.dumps({
            'workers': list(workers)
        }))

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        locations = Location.objects.all().values('location_description', 'temperature', 'O2_level')
        await self.send(text_data=json.dumps({
            'locations': list(locations)
        }))
