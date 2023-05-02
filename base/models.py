from django.db import models
from django.contrib.auth.models import User

# Create your models here. class will create table in Django database
class Topic(models.Model):
    name = models.CharField(max_length = 200)
    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    # if Topic is defined under Room then it has to be wrap in 'Topic'
    
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    #create the relationship between - because the User get call just above - then we set up the related_name

    updated =models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 
    #this set only first time data created - wil not be changed

    class Meta:
        ordering = ["-updated", "-created"]
        #without "-" the printout will be in DESC order

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # models.cascade means when the room is deleted then all messages are also got deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:50]