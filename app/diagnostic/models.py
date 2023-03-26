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

    def diagnostic_info(self)->hash:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'diagnostic_type': self.diagnostic_type,
            'started': self.started.ctime(),
            'ended': self.ended.ctime() if self.ended else '',
            'answers': self.answers
        }

class Recomendation(models.Model):
    index = models.IntegerField()
    diagnostic_type = models.TextField(default="standard", max_length=15, blank=False)
    competence_lvl = models.IntegerField(default=1)
    level_1 = models.TextField(default='', blank=False)
    level_2 = models.TextField(default='', blank=False)
    level_3 = models.TextField(default='', blank=False)

    def __str__(self):
        return f"{self.id}, {self.index}, {self.diagnostic_type}, {self.level_1}, {self.level_2}, {self.level_3}"