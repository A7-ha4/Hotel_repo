from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Booking
from django.contrib.auth.decorators import login_required
from datetime import datetime, date

def view_rooms(request):
    today = date.today()

    # All rooms
    all_rooms = Room.objects.all()

    # Future bookings
    future_bookings = Booking.objects.filter(check_out__gte=today)

    # Rooms booked by the current user
    my_bookings = future_bookings.filter(user=request.user) if request.user.is_authenticated else Booking.objects.none()
    my_rooms_ids = my_bookings.values_list('room_id', flat=True)

    # All booked room IDs
    booked_room_ids = future_bookings.values_list('room_id', flat=True)

    # Rooms not booked by anyone
    available_rooms = Room.objects.exclude(id__in=booked_room_ids)

    # Rooms booked by others
    unavailable_rooms = Room.objects.filter(id__in=booked_room_ids).exclude(id__in=my_rooms_ids)

    return render(request, 'rooms.html', {
        'available_rooms': available_rooms,
        'unavailable_rooms': unavailable_rooms,
        'my_bookings': my_bookings
    })

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']

        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

        days = (check_out_date - check_in_date).days
        total_price = days * room.price_per_night

        Booking.objects.create(
            user=request.user,
            room=room,
            check_in=check_in_date,
            check_out=check_out_date,
            total_price=total_price
        )

        return redirect('rooms')

    return render(request, 'book.html', {'room': room})

def dashboard(request):
    return render(request, 'home.html')
