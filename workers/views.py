from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Worker, Location
from .serializers import WorkerSerializer, LocationSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@api_view(['GET'])
def get_all_locations(request):
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def get_all_workers(request):
    workers = Worker.objects.all()
    serializer = WorkerSerializer(workers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def end_shift(request):
    
    workers = Worker.objects.all()
    locations=Location.objects.all()
    
    workers.update(location=None)
    locations.update(number_of_workers=0)

    return Response({'message': 'Shift ended successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_location(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_worker(request):
    data = request.data

    print("Received data:", data)
    
    if Worker.objects.filter(id=data.get('id')).exists():
        return Response({'error': 'Worker with this ID already exists'}, status=status.HTTP_400_BAD_REQUEST)

    
    if 'location' in data and data['location']:
        try:
            location = Location.objects.get(id=data['location'])
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        location = None  

    
    serializer = WorkerSerializer(data=data)
    if serializer.is_valid():
        worker = serializer.save()

        
        if location:
            location.number_of_workers += 1
            location.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_attendence(request):
    data = request.data
    worker_id=request.data['worker_id']
    try:
        worker = Worker.objects.get(id=worker_id)
    except Worker.DoesNotExist:
        return Response({'error': 'Worker not found'}, status=status.HTTP_404_NOT_FOUND)
    worker.available = not worker.available
    if not worker.available:
        worker.location = None
    worker.save()
    return Response({'message': 'Attendence updated successfully'}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_data(request):
    data = request.data  
    if not isinstance(data, list):
        return Response({'error': 'Data should be a list of workers'}, status=status.HTTP_400_BAD_REQUEST)
    updated_workers = []
    updated_locations = []
    errors = []
    for update_data in data:
        if update_data.get('update_type') == 'worker':
            worker_data = update_data
            worker_id = worker_data.get('worker_id')
            location_id = worker_data.get('location_id')
            sos_bit = worker_data.get('sos_bit')
            if not worker_id or not location_id:
                errors.append({
                    'error': 'Worker ID and Location ID are required for update',
                    'data': worker_data
                })
                continue
            try:
                worker = Worker.objects.get(id=worker_id)
            except Worker.DoesNotExist:
                errors.append({'error': 'Worker not found', 'worker_id': worker_id})
                continue
            if not worker.available:
                errors.append({'error': 'Worker is not available', 'worker_id': worker_id})
                continue
                    
            try:
                new_location = Location.objects.get(id=location_id)
            except Location.DoesNotExist:
                errors.append({'error': 'New location not found', 'worker_id': worker_id, 'location_id': location_id})
                continue
                
            worker.location = new_location
            worker.sos = sos_bit
            worker.save()
            updated_workers.append({
                'worker_id': worker_id,
                'new_location_id': location_id
            })
        else:
            location_id = update_data.get('location_id')
            if not location_id:
                errors.append({
                    'error': 'Location ID is required for location update',
                    'data': update_data
                })
                continue
                
            try:
                location = Location.objects.get(id=location_id)
            except Location.DoesNotExist:
                errors.append({'error': 'Location not found', 'location_id': location_id})
                continue
            
            # List of updatable location fields
            location_fields = [
                'description', 'temperature', 'humidity', 'pm10_level',
                'pm25_level', 'pm1_level', 'o2_level', 'emergency_bit'
            ]
            
            # Update location fields if provided
            updated_fields = {}
            for field in location_fields:
                if field in update_data:
                    setattr(location, field, update_data[field])
                    updated_fields[field] = update_data[field]
            
            location.save()
            
            updated_locations.append({
                'location_id': location_id,
                'updated_fields': updated_fields
            })
            
    response_data = {
        'updated_workers': updated_workers,
        'updated_locations': updated_locations
    }

    if errors:
        response_data['errors'] = errors
        return Response(response_data, status=status.HTTP_207_MULTI_STATUS)

    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['PUT'])
def update_worker(request, worker_id):
    try:
        
        worker = Worker.objects.get(id=worker_id)
    except Worker.DoesNotExist:
        return Response({'error': 'Worker not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    
    try:
        new_location = Location.objects.get(id=data['location'])
    except Location.DoesNotExist:
        return Response({'error': 'New location not found'}, status=status.HTTP_404_NOT_FOUND)

    
    if 'id' in data:
        del data['id']  

    
    worker_serializer = WorkerSerializer(worker, data=data, partial=True)  
    if worker_serializer.is_valid():
        worker_serializer.save()  
        return Response(worker_serializer.data)

    return Response(worker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_worker(request, worker_id):
    try:
        worker = Worker.objects.get(id=worker_id)
        

        worker.delete()  

        return Response({'message': 'Worker deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Worker.DoesNotExist:
        return Response({'error': 'Worker not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_location(request, location_id):
    try:
        location = Location.objects.get(id=location_id)
        workers = Worker.objects.filter(location=location)

        
        workers.update(location=None)

        location.delete()
        return Response({'message': 'Location deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Location.DoesNotExist:
        return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def worker_list(request):
    if request.method == 'GET':
        
        workers = Worker.objects.all()
        serializer = WorkerSerializer(workers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def location_list(request):
    if request.method == 'GET':
        
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)