from django.db import models
from django.contrib.auth.hashers import check_password


# Create your models here.
class UserModel(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=300, blank=False)

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        db_table = "users"
