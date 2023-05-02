from rest_framework.decorators import api_view
from rest_framework.response import Response
#from django.http import JsonResponse
from base.models import Room
from .serializers import RoomSerializer

@api_view(["GET"]) # allow use more methods "POST", "PUT"
def getRoutes(request):
    routes = [
        "GET /api",
        "GET /api/rooms",
        "GET /api/rooms/:id"
    ]
    return Response(routes)
#only JSON -> return JsonResponse(routes, safe=False)

@api_view(["GET"])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many = True)
    return Response(serializer.data)
    #objects cannot convert automatically to Response - we need to serialize them

@api_view(["GET"])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many = False)
    return Response(serializer.data)
    #objects cannot convert automatically to Response - we need to serialize them

    