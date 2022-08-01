from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Entry(models.Model):
    WORKING_HOURS = (
         (1.0, '1 Day'),
         (0.5, '0.5 Day'),
         (1.5, '1.5 Day'),
    )

    working_hours = models.FloatField(choices=WORKING_HOURS, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField(max_length=500)
    day = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.__str__()
