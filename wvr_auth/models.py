from django.db import models
from django.contrib.auth.models import User
from django.core.validators import ValidationError, validate_email
from utils.utils.misc import gen_random_str
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

