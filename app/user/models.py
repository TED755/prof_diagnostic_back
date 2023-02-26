from django.db import models

class User(models.Model):
    name = models.TextField(max_length=200, blank= False)
    email = models.EmailField(max_length=50, blank=False)
    password = models.TextField(max_length=100, blank=False)

class ActiveSession(models.Model):
    user_id = models.IntegerField(blank=False)
    access_token = models.CharField(max_length=500, blank=False)
    refresh_token = models.CharField(max_length=500, blank=False)
    started_at = models.DateTimeField()