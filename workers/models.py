from django.db import models

class Location(models.Model):
    id = models.CharField(max_length=4, unique=True, primary_key=True)
    description = models.CharField(max_length=255)
    number_of_workers = models.IntegerField(default=0)
    temperature = models.FloatField()
    o2_level = models.FloatField()
    emergency_bit = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        # When a location is deleted, set the location of all workers at this location to null
        workers = Worker.objects.filter(location=self)
        for worker in workers:
            worker.location = None
            worker.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.description


class Worker(models.Model):
    id = models.CharField(max_length=10, primary_key=True)  # Change this to CharField for custom IDs
    name = models.CharField(max_length=100)  # Name of the worker
    age = models.IntegerField()  # Age of the worker
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)  # Reference to the Location model

    def delete(self, *args, **kwargs):
        # When a worker is deleted, decrease the worker count of their location
        if self.location:
            self.location.number_of_workers -= 1
            self.location.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
