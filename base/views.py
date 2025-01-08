from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Room , Topic , Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import time

def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password') 

        try:
            user = User.objects.get(username = username)

        except:
            messages.error(request, "User does not exist")

        user = authenticate(request , username= username , password = password)

        if user is not None :
            login(request , user)
            return redirect('home')

        else:
            messages.error(request, "Username or Password does not exist")   

    context = {'page': page}
    return render( request , 'base/login_register.html' , context)

def logoutpage (request):
    logout(request)
    return redirect('home')

def registerpage(request):
    form = UserCreationForm()
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid ():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request , user)
            return redirect('home')
        else:
            messages.error(request, "Something went wrong please try again later... :(")

             

    context = {'form':form}
    return render(request , 'base/login_register.html', context )

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) 
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms , 'topics':topics ,'room_count': room_count}
    return render(request , 'base/home.html' ,context)


def room(request , pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('created')
    
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')

        )
        return redirect('room',pk = room.id)

    context = {'room': room , 'room_messages':room_messages }        
    return render(request , 'base/room.html' , context)

    
@login_required(login_url = '/login')


def createRoom(request):

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('home')


    context = {'form': form ,'topics' : topics}
    return render(request , 'base/room_form.html' , context) 


@login_required(login_url = '/login')
def updateRoom(request, pk):
    host = request.user
    room = Room.objects.get(id = pk) 
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        
        if form.is_valid():
             form.save()
         
        form = RoomForm(request.POST, instance= room)
        return redirect('home')

        
    context =  {'form':form  ,'topics' : topics }
    return render(request , 'base/room_form.html' ,context)

@login_required(login_url = '/login')
def delete_room (request , pk):
    room = Room.objects.get(id = pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'object' : room})

@login_required(login_url = '/login')
def profilepage(request):
    #user = User.objects.get(id= pk)
    #rooms = user.room_set.all()
    #context = {'user' : user , 'rooms': rooms}
    return render(request , 'base/profile.html ') # , context