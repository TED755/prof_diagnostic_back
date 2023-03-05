from datetime import timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

class Diagnostic(models.Model):
    user_id = models.IntegerField(blank=False)
    diagnostic_type = models.TextField(default="standard", max_length=15, blank=False)
    started = models.DateTimeField(default=timezone.now, blank=True)
    ended = models.DateTimeField(blank=True, null=True)
    answers = ArrayField(base_field=models.IntegerField(blank=True, default=0, null=True), size=45, null=True)