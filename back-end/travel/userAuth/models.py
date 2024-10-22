from django.db import models


# Create your models here.
class UserModel(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=300, blank=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
