from django.http import Http404, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import render,redirect

from .models import Room,Topic,Message,User 
# from django.contrib.auth.models import User

# from django.contrib.auth.forms import UserCreationForm

from .forms import RoomForm
from django.contrib.auth import authenticate, login,logout

# Create your views here.
from .forms import RoomForm, UserForm, MyUserCreationForm
def loginPage(request):
    page = "login"
    
    
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not exist")

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form =  MyUserCreationForm(request.POST)
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'An error occurred during registration') 
                
    return render(request, 'base/login_register.html',{'form':form})

def home(request):
    q = request.GET.get('q','') if request.GET.get('q') != None else '' 
    rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
)

    topic = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    return render(request, 'base/home.html',{'rooms':rooms,
                                            'topics':topic,'room_count':room_count,
                                            "room_messages":room_messages})


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)




def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
            'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

 
@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        
        Room.objects.create(
            host = request.user,
            topic = topic, 
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            
        )
        return redirect('home')
        #print(request.POST)
    context = {'form':form,'topics':topics}
    return render(request,'base/room_form.html', context)

@login_required(login_url = 'login')
def updateRoom(request,pk):
    room = Room.objects.get(id =pk)
    form = RoomForm(instance=room)
    topics= Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context ={'form':form,'topics':topics,'room':room}
    return render(request, 'base/room_form.html',context)



from django.http import Http404
@login_required(login_url = 'login')
def deleteRoom(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise Http404("Room does not exist")
    
    if request.user != room.host:
        return HttpResponse('You are not allowed to Delete this Room!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url = 'login')
def deleteMessage(request, room_id):
    try:
        message = Message.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise Http404("Room does not exist")
    
    if request.user != message.user:
        return HttpResponse('You are not delete this Message, you can delete this message!!')
    
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance = user)
    
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES,instance = user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk= user.id)
    context = {'form':form}
    return render(request,'base/update-user.html',context)

def topicsPage(request):
    q = request.GET.get('q','') if request.GET.get('q') != None else '' 
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html',{'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request,'base/activity.html',{'room_messages': room_messages})