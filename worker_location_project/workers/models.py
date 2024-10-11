from django.db import models

class Location(models.Model):
    id = models.CharField(max_length=4, unique=True, primary_key=True)
    description = models.TextField()
    number_of_workers = models.IntegerField(default=0)
    temperature = models.FloatField()
    o2_level = models.FloatField()
    emergency_bit = models.BooleanField(default=False)

    def __str__(self):
        return self.description

class Worker(models.Model):
    id = models.CharField(max_length=4, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    location = models.ForeignKey(Location, related_name='workers', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
