from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class AccountType(models.TextChoices):
        READER = 'reader', 'Reader'
        WRITER = 'writer', 'Writer'
    
    email = models.EmailField(unique=True)
    pen_name = models.CharField(max_length=300, unique=True, blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    profile_picture = models.ImageField(upload_to="profile/%Y/%M/%d", blank=True, default='default.jpg')
    account_type = models.CharField(max_length=6,choices=AccountType.choices, default=AccountType.READER)
    writer_bio = models.TextField(blank=True)
    genres = models.CharField(max_length=255)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
