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
    # Check if the worker with the given ID already exists
    if Worker.objects.filter(id=data.get('id')).exists():
        return Response({'error': 'Worker with this ID already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # If location is provided, handle it; if not, skip
    if 'location' in data and data['location']:
        try:
            location = Location.objects.get(id=data['location'])
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        location = None  # Set location to None if not provided

    # Create the worker
    serializer = WorkerSerializer(data=data)
    if serializer.is_valid():
        worker = serializer.save()

        # If a location was provided, update the worker count
        if location:
            location.number_of_workers += 1
            location.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_worker(request, worker_id):
    try:
        # Try to get the worker by id, if not found, return an error
        worker = Worker.objects.get(id=worker_id)
    except Worker.DoesNotExist:
        return Response({'error': 'Worker not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    # Ensure the new location exists
    try:
        new_location = Location.objects.get(id=data['location'])
    except Location.DoesNotExist:
        return Response({'error': 'New location not found'}, status=status.HTTP_404_NOT_FOUND)

    # Exclude the worker's ID from the update data to avoid creating new workers
    if 'id' in data:
        del data['id']  # Prevent 'id' from being modified

    # Update worker's details
    worker_serializer = WorkerSerializer(worker, data=data, partial=True)  # Use partial=True to allow partial updates
    if worker_serializer.is_valid():
        # Check if the location did not existed before
        if not worker.location:
            new_location.number_of_workers += 1
            new_location.save()
        # Check if the location is being changed
        if worker.location.id != new_location.id:
            old_location = worker.location
            if old_location:
                old_location.number_of_workers -= 1
                old_location.save()

            new_location.number_of_workers += 1
            new_location.save()

        worker_serializer.save()  # Save the updated worker
        return Response(worker_serializer.data)

    return Response(worker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_worker(request, worker_id):
    try:
        worker = Worker.objects.get(id=worker_id)
        # location = worker.location

        worker.delete()  # Delete the worker
        # Decrease worker count at the old location
        # if location:
        #     location.number_of_workers -= 1
        #     location.save()

        return Response({'message': 'Worker deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Worker.DoesNotExist:
        return Response({'error': 'Worker not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_location(request, location_id):
    try:
        location = Location.objects.get(id=location_id)
        workers = Worker.objects.filter(location=location)

        # Set the location of associated workers to None
        workers.update(location=None)

        location.delete()
        return Response({'message': 'Location deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Location.DoesNotExist:
        return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def worker_list(request):
    if request.method == 'GET':
        # Retrieve all workers
        workers = Worker.objects.all()
        serializer = WorkerSerializer(workers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Add a new worker
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def location_list(request):
    if request.method == 'GET':
        # Retrieve all locations
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Add a new location
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)