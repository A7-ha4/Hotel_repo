from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Booking
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Room

def view_rooms(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'rooms.html', {'rooms': rooms})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_available=True)

    if request.method == 'POST':
        # Access form data using the updated field names
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']

        # Convert to date objects
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

        # Days of stay
        days = (check_out_date - check_in_date).days
        total_price = days * room.price_per_night

        # Create booking
        Booking.objects.create(
            user=request.user,
            room=room,
            check_in=check_in_date,
            check_out=check_out_date,
            total_price=total_price
        )

        # Optionally mark room unavailable
        room.is_available = False
        room.save()

        return redirect('rooms')  # Redirect to the view where rooms are listed

    return render(request, 'book.html', {'room': room})

def dashboard(request) :
    return render(request, 'home.html')

