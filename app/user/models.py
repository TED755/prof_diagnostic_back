from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.TextField(max_length=200, blank= False)
    email = models.EmailField(max_length=50, blank=False)
    password = models.TextField(max_length=100, blank=False)
    category = models.TextField(max_length=50, blank=True)
    teaching_exp = models.TextField(max_length=50, blank=True)
    position = models.TextField(max_length=50, blank=True)
    raion = models.TextField(max_length=50, blank=True)
    region_rf = models.TextField(max_length=50, blank=True)
    school = models.TextField(max_length=50, blank=True)
    locality_type = models.TextField(max_length=50, blank=True)

class ActiveSession(models.Model):
    user_id = models.IntegerField(blank=False)
    expired = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

# class Diagnostic(models.Model):
#     user_id = models.IntegerField(blank=False)
#     diagnostic_type = models.TextField(default="standard", max_length=15, blank=False)
#     answers = ArrayField(base_field=models.IntegerField(blank=True, default=0), size=45)