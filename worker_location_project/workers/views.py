from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Worker, Location
from .serializers import WorkerSerializer, LocationSerializer

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

    # Check if the worker with the given ID already exists
    if Worker.objects.filter(id=data['id']).exists():
        return Response({'error': 'Worker with this ID already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Try to get the location
    try:
        location = Location.objects.get(id=data['location'])
    except Location.DoesNotExist:
        return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

    # Now that we know the worker doesn't exist and the location is valid, try to add the worker
    serializer = WorkerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

        # Increment the location's worker count after successfully adding the worker
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
