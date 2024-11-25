import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class WorkerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.stream_task = asyncio.create_task(self.stream_workers())

    async def disconnect(self, close_code):
        
        self.stream_task.cancel()

    async def stream_workers(self):
        while True:
            try:
                
                workers = await self.get_workers()
                await self.send(text_data=json.dumps({
                    'workers': workers
                }))
                
                await asyncio.sleep(5)  
            except asyncio.CancelledError:
                
                break

    @database_sync_to_async
    def get_workers(self):
        from .models import Worker
        
        return list(Worker.objects.select_related('location').values('id','name', 'age', 'location_id', 'sos', 'available', 'aadhar'))
class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.stream_task = asyncio.create_task(self.stream_locations())

    async def disconnect(self, close_code):
        
        self.stream_task.cancel()

    async def stream_locations(self):
        while True:
            try:
                
                locations = await self.get_locations()
                await self.send(text_data=json.dumps({
                    'locations': locations
                }))
                
                await asyncio.sleep(5)  
            except asyncio.CancelledError:
                
                break

    @database_sync_to_async
    def get_locations(self):
        from workers.models import Location
        
        return list(Location.objects.values('id','description', 'temperature', 'humidity','number_of_workers','emergency_bit','available', 'pm10_level', 'pm25_level', 'pm1_level', 'o2_level','x','y'))
