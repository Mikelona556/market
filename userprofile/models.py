from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    pix = models.ImageField(upload_to= 'Profile', default='avatar.jpg')

    def _str_(self):
        return self.User.username