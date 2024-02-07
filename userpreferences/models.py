from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserPreference(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, blank=True, null=True, default='USD')
    
    def _str_(self):
        return str(self.user) + 's' + 'preferences'
    
    class Meta:
        verbose_name_plural = 'User Preferences'