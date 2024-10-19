# workers/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class WorkerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Import Worker model here
        from .models import Worker
        # workers = Worker.objects.all().values('name', 'age', 'location_description')
        # await self.send(text_data=json.dumps({
        #     'workers': list(workers)
        # }))
        # workers = await database_sync_to_async(self.get_workers)()
        # await self.send(text_data=json.dumps({
        #     'workers': workers
        # }))
        print("Receiving data:", text_data)
        data = json.loads(text_data)
    # Check if the action is to get workers
        # if data.get('action') == 'get_workers':
        #     print("Fetching workers...")
        # Fetch workers from the database asynchronously
        workers = await self.get_workers()
        print("Workers fetched:", workers)
        await self.send(text_data=json.dumps({
                'workers': workers
        }))
    @database_sync_to_async
    def get_workers(self):
        from .models import Worker
        # This runs in a synchronous context
        return list(Worker.objects.select_related('location').values('name', 'age', 'location__description'))
        #return list(Worker.objects.values('name', 'age'))
  

    
class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Import Location model here
        from .models import Location
        # locations = Location.objects.all().values('location_description', 'temperature', 'O2_level')
        # await self.send(text_data=json.dumps({
        #     'locations': list(locations)
        # }))
        locations = await database_sync_to_async(self.get_locations)()
        await self.send(text_data=json.dumps({
            'locations': locations
        }))

    @database_sync_to_async
    def get_locations(self):
        from .models import Location
        # This runs in a synchronous context
        return list(Location.objects.values('location_description', 'temperature', 'O2_level'))