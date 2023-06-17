from django.contrib import admin
from .models import Studio, Engineer, Artist, Booking, Schedule

# Register your models here.
admin.site.register(Studio)
admin.site.register(Engineer)
admin.site.register(Artist)
admin.site.register(Booking)
admin.site.register(Schedule)
