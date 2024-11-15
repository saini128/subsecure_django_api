from django.contrib import admin
from .models import Location, Worker, SafeLevels


admin.site.site_header = "SubSecure Administration"
admin.site.site_title = "SubSecure Admin Portal"
admin.site.index_title = "Welcome to SubSecure Admin"
admin.site.register(Location)
admin.site.register(Worker)
admin.site.register(SafeLevels)
