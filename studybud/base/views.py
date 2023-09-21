from django.shortcuts import render

# Create your views here.
#from django.http import HttpResponse

rooms =[
    {"id":1,'name':'lets learn python'},
    {"id":2,'name':'lets learn Django'},
    {"id":3,'name':'let learn programming language'},
]

def home(request):
    context ={'rooms':rooms}
    return render(request,'base/home.html',context)

def room(request, pk):
    return render(request,'base/room.html')
