from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator



User = get_user_model()

class Message(models.Model):
    message = models.JSONField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)

class Location(models.Model):
    id = models.CharField(max_length=4, unique=True, primary_key=True)
    description = models.CharField(max_length=255)
    number_of_workers = models.IntegerField(default=0)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    pm10_level = models.FloatField(null=True, blank=True)
    pm25_level = models.FloatField(null=True, blank=True)
    pm1_level = models.FloatField(null=True, blank=True)
    o2_level = models.FloatField(null=True, blank=True)
    emergency_bit = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        
        workers = Worker.objects.filter(location=self)
        for worker in workers:
            worker.location = None
            worker.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.description

class SafeLevels(models.Model):
    pm10_min = models.FloatField()
    pm10_max = models.FloatField()
    pm25_min = models.FloatField()
    pm25_max = models.FloatField()
    pm1_min = models.FloatField()
    pm1_max = models.FloatField()
    o2_min = models.FloatField()
    o2_max = models.FloatField()
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    humidity_min = models.FloatField()
    humidity_max = models.FloatField()
    
    def __str__(self):
        return "Safe Levels"

class Worker(models.Model):
    id = models.CharField(max_length=10, primary_key=True)  
    name = models.CharField(max_length=100)  
    age = models.IntegerField()  
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='workers')  
    sos = models.BooleanField(default=False)  

    def delete(self, *args, **kwargs):
        
        if self.location:
            self.location.number_of_workers -= 1
            self.location.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=Location)
def update_emergency_bit(sender, instance, **kwargs):
    
    safe_levels = SafeLevels.objects.first()
    if not safe_levels:
        return  

    
    emergency = (
        (instance.temperature is not None and (instance.temperature < safe_levels.temperature_min or instance.temperature > safe_levels.temperature_max)) or
        (instance.humidity is not None and (instance.humidity < safe_levels.humidity_min or instance.humidity > safe_levels.humidity_max)) or
        (instance.pm10_level is not None and (instance.pm10_level < safe_levels.pm10_min or instance.pm10_level > safe_levels.pm10_max)) or
        (instance.pm25_level is not None and (instance.pm25_level < safe_levels.pm25_min or instance.pm25_level > safe_levels.pm25_max)) or
        (instance.pm1_level is not None and (instance.pm1_level < safe_levels.pm1_min or instance.pm1_level > safe_levels.pm1_max)) or
        (instance.o2_level is not None and (instance.o2_level < safe_levels.o2_min or instance.o2_level > safe_levels.o2_max))
    )

    
    if instance.emergency_bit != emergency:
        instance.emergency_bit = emergency
        instance.save(update_fields=["emergency_bit"])

@receiver(post_save, sender=Worker)
def update_worker_count_on_save(sender, instance, **kwargs):
    if instance.location:
        location = instance.location
        location.number_of_workers = location.workers.count()
        location.save(update_fields=["number_of_workers"])


@receiver(pre_delete, sender=Worker)
def update_worker_count_on_delete(sender, instance, **kwargs):
    if instance.location:
        location = instance.location
        location.number_of_workers = location.workers.count() - 1  # Reduce count by 1
        location.save(update_fields=["number_of_workers"])