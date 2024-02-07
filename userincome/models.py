from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class UserIncome(models.Model):
    source = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.FloatField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(default = now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.source

class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name