from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
#from django.contrib.auth.models import User -- with custom user this line is not needed
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Create your views here.

""" rooms = [
    {"id":1, "name":"Let's learn Python!"},
    {"id":2, "name":"Design with me."},
    {"id":3, "name":"Frontend developer"}
] """

def loginPage(request): 
    #set page to check the value for login or register - if page is login then show register else show login
    page = "login"

    #avoid the user to re-login - if the user has been login - on the tab try localhost:8000/login - it remains on the  home page
    if request.user.is_authenticated:
        return redirect("home")

    #should not user login because of build in function has that name
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        # check if the user is already existed
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist.")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or Password is not correct.")
        
    context = {"page":page}
    return render(request, 'base/login_register.html', context )

def logoutUser(request):
    logout(request) #auto delete token
    return redirect("home")

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #freeze the save to wait for setting up the right format
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration. Please try again...")

    return render(request, "base/login_register.html", {"form":form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # if not None then get "q" - else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q))
    # .get() - .filter() - .all() -  .exclude()....
    # __icontains will execute whatever we have in "q" - ex: q = "Py" it will automatically search for all contains "Py" - with "i" will take all case even Upper or lower

    topics = Topic.objects.all()[0:5]
    #limit topic item show on the homepage to 5
    room_count = rooms.count()
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
    "rooms": rooms,
    "topics":topics,
    "room_count":room_count,
    "room_message":room_message}
    
    return render(request, "base/home.html", context )

def room(request, pk):
    room = Room.objects.get(id=pk)
   
    room_messages = room.message_set.all().order_by("-created")
    #"_set.all()" get all messages query from the child of specific Room -> class Message via the comment "message_set.all()"

    participants = room.participants.all()
    
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)

    context = {"room":room, "room_messages": room_messages, "participants": participants}

    return render(request, "base/room.html", context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    #"_set.all()" _set queries to get all values

    room_message = user.message_set.all()
    topics = Topic.objects.all()

    context = {"user":user, "rooms":rooms, "topics": topics, "room_message": room_message}
    return render(request, "base/profile.html", context)

@login_required(login_url = "login")
# user need to login to use the createRoom function

def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")

        #if value is exist - created will be false
        topic, created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description = request.POST.get("description")
        )

        return redirect("home")
    context = {"form":form, "topics":topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = "login")
# user need to login to use the updateRoom function

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    # instance fill up the form with room values

    if request.user != room.host:
        #With "frank" login - frank cannot edit "thanh" room
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")

        #if value is exist - created will be false
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        
        return redirect("home")

    context = {"form":form, "topics":topics, "room":room}
    return render(request, "base/room_form.html", context)

@login_required(login_url = "login")
# user need to login to use the deleteRoom function

def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj":room})

@login_required(login_url = "login")
# user need to login to use the deleteRoom function

def deleteMessage(request, pk):
    message = Message.objects.get(id = pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj":message})

@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=user.id)

    return render(request, "base/update-user.html",{"form":form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains = q)
    return render(request, 'base/topics.html',{"topics":topics})

def activityPage(request):
    room_message = Message.objects.all()
    return render(request, "base/activity.html",{"room_message": room_message})