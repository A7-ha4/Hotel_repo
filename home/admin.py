from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price_per_night', 'is_available')
    search_fields = ('room_number', 'room_type')
    list_filter = ('is_available', 'room_type')

admin.site.register(Booking)
