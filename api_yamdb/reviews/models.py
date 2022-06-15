from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    ANONYMOUS = 'ANON'
    USER = 'USER'
    MODERATOR = 'MOD'
    ADMIN = 'ADM'
    ROLES = [ 
        (ANONYMOUS, 'Anonymous'),
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    ]
    
    role = models.CharField(
        max_length=4,
        choices=ROLES,
        default=USER,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    def __str__(self):
        return self.username