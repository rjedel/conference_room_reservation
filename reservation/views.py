from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from .models import Room


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
            return redirect('/rooms/')


def rooms_view(request):
    return render(request, 'reservation/rooms.html', context={'rooms': Room.objects.all()})


def room_delete_by_id_view(request, id):
    try:
        room = Room.objects.get(pk=id)
    except Room.DoesNotExist:
        raise Http404
    else:
        room.delete()
        return redirect('/rooms/')


def room_modify_by_id_view(request, id):
    try:
        room = Room.objects.get(pk=id)
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
                message = f"room '{name}' already exists, choose a different name"
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
                return redirect('/rooms/')
