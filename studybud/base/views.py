from django.shortcuts import render
from .models import Room
# Create your views here.


def home(request):
    rooms = Room.objects.all() 
    return render(request, 'base/home.html',{'rooms':rooms})
def room(request, pk): #primary key
    room = Room.objects.get(id = pk)
    return render(request,'base/room.html', {'room': room})

def createRoom(request):
    context = {}
    return render(request,'base/room_form.html')
