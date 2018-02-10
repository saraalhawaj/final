from django.db import models
from django.utils import timezone  
from django.utils.http import urlquote  
from django.core.mail import send_mail  
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):  
	major_choices = (('Industrial', 'Industrial'), ('Electrical', 'Electrical'),('Computer', 'Computer'))
	major = models.CharField(('major choices '), max_length=30, blank=False, choices=major_choices)
	course_choices = (('operating system', 'operating system'), ('physics', 'physics'),('nano', 'nano'))
	course = models.CharField(('course choices '), max_length=30, blank=False, choices=course_choices)


class Myfeed(models.Model):

    username = models.CharField(max_length=255)
    book = models.ImageField(null=True, blank=True)
    feed = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    major_choices = (('Industrial', 'Industrial'), ('Electrical', 'Electrical'),('Computer', 'Computer'))
    major = models.CharField(('major choices '), max_length=30, blank=False, choices=major_choices)
    course_choices = (('operating system', 'operating system'), ('physics', 'physics'),('nano', 'nano'))
    course = models.CharField(('course choices '), max_length=30, blank=False, choices=course_choices)



    def __str__(self):
        return self.username
class Like(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	myfeed = models.ForeignKey(Myfeed, on_delete=models.CASCADE)

class Reply(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	myfeed = models.ForeignKey(Myfeed, on_delete=models.CASCADE)
	reply = models.TextField()
 

class Message(models.Model):
    text = models.TextField(max_length=700)
    time = models.DateTimeField(auto_now=True, auto_now_add=False)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, blank=True, related_name="user")
    recipient = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, blank=True, related_name="recipient")
    def __str__(self):
        return self.text
