from django.http import HttpResponse
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
            return redirect('/')


def rooms_view(request):
    return render(request, 'reservation/rooms.html', context={'rooms': Room.objects.all()})


def room_delete_by_id_view(request, id):
    try:
        room = Room.objects.get(pk=id)
    except Room.DoesNotExist:
        return HttpResponse('no room id {}'.format(id))
    else:
        room.delete()
        return redirect('/rooms/')
