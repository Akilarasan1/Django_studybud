from django.http import Http404, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import render,redirect
from .models import Room, Topic, CustomMessage
from django.contrib.auth.models import User
from .forms import RoomForm
from django.contrib.auth import authenticate, login,logout

# Create your views here.
from .forms import RoomForm

from django.contrib.auth import authenticate, login

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not exist")

    context = {}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q','') if request.GET.get('q') != None else ' ' 
    rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
)

    topic = Topic.objects.all()
    room_count = rooms.count()
    return render(request, 'base/home.html',{'rooms':rooms,
                                            'topics':topic,'room_count':room_count})

def room(request, pk): #primary key
    room = Room.objects.get(id = pk)
    return render(request,'base/room.html', {'room': room})

@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        #print(request.POST)
    context = {'form':form}
    return render(request,'base/room_form.html', context)

@login_required(login_url = 'login')

def updateRoom(request,pk):
    room = Room.objects.get(id =pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context ={'form':form}
    return render(request, 'base/room_form.html',context)



from django.http import Http404
@login_required(login_url = 'login')
def deleteRoom(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise Http404("Room does not exist")

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


    
# def deleteRoom(reque st, pk):
    # room = Room.objects.get(id=pk)

    # if request.method == 'POST':
        # room.delete()
        # return redirect('home')

    # return render(request, 'base/delete.html', {'obj': room})
