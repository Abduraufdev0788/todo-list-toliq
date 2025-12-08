from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES = [
        ("ADMIN", "Admin"),
        ("USER", "User"),
    ]

    roles = models.CharField(choices=ROLES, default="USER", max_length=15)


    @property
    def is_admin(self):
        return self.roles == 'ADMIN'

    @property
    def is_user(self):
        return self.roles == 'USER'