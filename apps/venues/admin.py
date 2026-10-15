from django.contrib import admin
from .models import Venue
# Register your models here.
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "capacity", "is_active")
    list_filter = ("city", "is_active")
    search_fields = ("name", "address", "city")