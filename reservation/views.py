from datetime import datetime

from django.http import Http404
from django.shortcuts import render, redirect

from .models import Room, Reservation


def room_new_view(request):
    if request.method == 'GET':
        return render(request, 'reservation/room_new.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        message = ''
        if name is None or len(name) < 1:
            message = 'enter room name'
        if name in [room.name for room in Room.objects.all()]:
            message = 'this room already exists'
        try:
            if int(capacity) < 1:
                message = 'capacity must be greater than 1'
        except (ValueError, TypeError):
            message = 'enter an integer'
        if projector == "True":
            projector = True
        else:
            projector = False

        if message:
            return render(request, 'reservation/room_new.html', context={'message': message})
        else:
            Room.objects.create(name=name, capacity=int(capacity), projector=projector)
            return redirect('room-table')


def rooms_view(request):
    rooms = Room.objects.all()
    today = datetime.now().date()
    for room in rooms:
        reservation_dates = [reservation.date for reservation in room.reservations.all()]
        room.reserved = today in reservation_dates
    return render(request, 'reservation/rooms.html', context={'rooms': rooms, })


def room_delete_by_id_view(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise Http404
    else:
        room.delete()
        return redirect('room-table')


def room_modify_by_id_view(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise Http404
    else:
        if request.method == 'GET':
            return render(request, 'reservation/room_modify.html', context={'room': room})
        if request.method == 'POST':
            name = request.POST.get('name')
            capacity = request.POST.get('capacity')
            projector = request.POST.get('projector')
            message = ''
            if name is None or len(name) < 1:
                message = 'enter room name'
            other_rooms = Room.objects.exclude(name=room.name)
            if name in [room.name for room in other_rooms]:
                message = f"room '{name}' already exists"
            try:
                if int(capacity) < 1:
                    message = 'capacity must be greater than 1'
            except (ValueError, TypeError):
                message = 'enter an integer'
            if projector == "True":
                projector = True
            else:
                projector = False

            if message:
                return render(request, 'reservation/room_modify.html', context={'message': message, 'room': room})
            else:
                room.name = name
                room.capacity = int(capacity)
                room.projector = projector
                room.save()
                return redirect('room-table')


def room_reserve_by_id_view(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise Http404
    else:
        today = datetime.now().date()
        reservations = [_ for _ in room.reservations.order_by('date') if _.date >= today]
        if request.method == 'GET':
            return render(request, 'reservation/room_reserve.html', context={
                'room': room,
                'reservations': reservations,
            })
        if request.method == 'POST':
            date_form = request.POST.get('date')
            comment = request.POST.get('comment')
            date_user = datetime.strptime(date_form, "%Y-%m-%d").date()
            if date_user < today:
                return render(request, 'reservation/room_reserve.html', context={
                    'room': room,
                    'message': 'you can not reserve with a retrograde date',
                    'reservations': reservations,
                })
            if date_user in [_.date for _ in room.reservations.all() if _.date >= today]:
                return render(request, 'reservation/room_reserve.html', context={
                    'room': room,
                    'message': f'on {date_user}, the room is already reserved',
                    'reservations': reservations,
                })
            Reservation.objects.create(date=date_user, room=room, comment=comment)
            return redirect('room-table')


def room_details_view(request, room_id):
    today = datetime.now().date()

    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise Http404
    else:
        return render(request, 'reservation/room_details.html', context={
            'room': room,
            'reservations': [_ for _ in room.reservations.order_by('date') if _.date >= today],
        })


def search_view(request):
    today = datetime.now().date()
    name = request.GET.get("name")

    capacity = request.GET.get("capacity")
    capacity = int(capacity) if capacity else 0

    projector = request.GET.get('projector')

    rooms = Room.objects.all().order_by('name')
    if projector == "True":
        rooms = rooms.filter(projector=1)
    if projector == "notTrue":
        rooms = rooms.filter(projector=0)
    if capacity:
        rooms = rooms.filter(capacity__gte=capacity)
    if name:
        rooms = rooms.filter(name__contains=name)

    if len(rooms) == 0:
        message = 'No rooms available for the given search criteria'
    else:
        message = False

    for room in rooms:
        reservation_dates = [reservation.date for reservation in room.reservations.all()]
        room.reserved = today in reservation_dates

    return render(request, 'reservation/search.html', context={
        'rooms': rooms,
        'message': message,
        'name': name,
        'capacity': capacity,
        'projector': projector,
    })


def about_view(request):
    return render(request, 'reservation/about.html')
