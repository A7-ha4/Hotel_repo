
from django.urls import path
from .views import view_rooms, book_room, dashboard

urlpatterns = [
    path('rooms/', view_rooms, name='rooms'),
    path('booking/<int:room_id>/', book_room, name='booking'),
    path('booking/', book_room, name='booking'),
    path('', dashboard, name='home'),
]
