from django.shortcuts import render
from .models import Room
# Create your views here.
#from django.http import HttpResponse

# rooms =[
    # {"id":1,'name':'lets learn python'},
    # {"id":2,'name':'lets learn Django'},
    # {"id":3,'name':'lets learn programming language'},
#]


def home(request):
    rooms = Room.objects.all() 
    return render(request, 'base/home.html',{'rooms':rooms})
def room(request, pk): #primary key
    room = Room.objects.get(id = pk)
    return render(request,'base/room.html', {'room': room})


#def room(request, pk): #primary key
#   room = None
# for i in rooms:
#     if i['id'] == int(pk):
#        room = i
# return render(request,'base/room.html', {'room': room})
