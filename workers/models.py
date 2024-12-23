from concurrent.futures.thread import _worker
from datetime import datetime
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
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
    available = models.BooleanField(default=True)
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)

    
    def save(self, *args, **kwargs):
        # Logic to update emergency_bit based on safe levels
        safe_levels = SafeLevels.objects.first()
        if safe_levels:
            self.emergency_bit = (
                not (safe_levels.pm10_min <= self.pm10_level <= safe_levels.pm10_max) or
                not (safe_levels.pm25_min <= self.pm25_level <= safe_levels.pm25_max) or
                not (safe_levels.pm1_min <= self.pm1_level <= safe_levels.pm1_max) or
                not (safe_levels.o2_min <= self.o2_level <= safe_levels.o2_max) or
                not (safe_levels.temperature_min <= self.temperature <= safe_levels.temperature_max) or
                not (safe_levels.humidity_min <= self.humidity <= safe_levels.humidity_max)
            )
        super().save(*args, **kwargs)

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
    available = models.BooleanField(default=True)
    aadhar = models.CharField(max_length=12, null=True, blank=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_location_id = self.location_id if self.location_id else None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._original_location_id = self.location_id

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Worker)
def update_worker_counts_on_save(sender, instance, **kwargs):
    """
    Updates worker counts when a worker is saved, handling both old and new locations
    """
    # If the worker's location has changed, update both old and new locations
    if kwargs.get('update_fields') != frozenset(['location']):  # Prevent recursive saves
        # Update new location's count
        if instance.location:
            instance.location.number_of_workers = instance.location.workers.count()
            instance.location.save(update_fields=['number_of_workers'])
        
        # If this is an update (not a new worker), also update the old location's count
        if not kwargs.get('created', False) and hasattr(instance, '_original_location_id'):
            old_location_id = instance._original_location_id
            if old_location_id and old_location_id != instance.location_id:
                try:
                    old_location = Location.objects.get(id=old_location_id)
                    old_location.number_of_workers = old_location.workers.count()
                    old_location.save(update_fields=['number_of_workers'])
                except Location.DoesNotExist:
                    pass

@receiver(post_delete, sender=Worker)
def update_location_count_on_worker_delete(sender, instance, **kwargs):
    """
    Updates the location's worker count after a worker is deleted
    """
    if instance.location:
        instance.location.number_of_workers = instance.location.workers.count()
        instance.location.save(update_fields=['number_of_workers'])

def update_all_location_counts():
    """
    Utility function to update all location worker counts
    """
    for location in Location.objects.all():
        worker_count = location.workers.count()
        if location.number_of_workers != worker_count:
            location.number_of_workers = worker_count
            location.save(update_fields=['number_of_workers'])

# Add save method to Worker model to track location changes
class EventLog(models.Model):
    EVENT_TYPE_CHOICES = [
        ('EMERGENCY', 'Emergency Triggered'),
        ('SOS', 'SOS Triggered'),
    ]
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.event_type == 'EMERGENCY':
            return f"Emergency at Location: {self.location}"
        elif self.event_type == 'SOS':
            return f"SOS Triggered by Worker: {self.worker}"

# Signal to log emergency bit triggers
@receiver(pre_save, sender=Location)
def log_emergency_trigger(sender, instance, **kwargs):
    if instance.pk:
        previous = Location.objects.get(pk=instance.pk)
        if not previous.emergency_bit and instance.emergency_bit:
            EventLog.objects.create(
                event_type='EMERGENCY',
                timestamp=datetime.now(),
                location=instance,
                details=f"Location {instance.description} triggered emergency due to unsafe conditions."
            )

# Signal to log SOS button triggers
@receiver(pre_save, sender=Worker)
def log_sos_trigger(sender, instance, **kwargs):
    if instance.pk:
        previous = Worker.objects.get(pk=instance.pk)
        if not previous.sos and instance.sos:
            EventLog.objects.create(
                event_type='SOS',
                worker=instance,
                timestamp=datetime.now(),
                details=f"Worker {instance.name} triggered SOS at location {instance.location}."
            )