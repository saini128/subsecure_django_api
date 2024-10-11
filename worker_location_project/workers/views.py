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
    try:
        location = Location.objects.get(id=data['location'])
        location.number_of_workers += 1
        location.save()
    except Location.DoesNotExist:
        return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = WorkerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_worker(request, worker_id):
    try:
        worker = Worker.objects.get(id=worker_id)
    except Worker.DoesNotExist:
        return Response({'error': 'Worker not found'}, status=status.HTTP_404_NOT_FOUND)

    old_location = worker.location
    data = request.data
    new_location = Location.objects.get(id=data['location'])

    # Update worker's location
    worker_serializer = WorkerSerializer(worker, data=data)
    if worker_serializer.is_valid():
        worker_serializer.save()

        # Update the worker counts in both old and new locations
        old_location.number_of_workers -= 1
        old_location.save()
        new_location.number_of_workers += 1
        new_location.save()

        return Response(worker_serializer.data)
    return Response(worker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
