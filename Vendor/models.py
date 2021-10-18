from django.db import models

class Vendors(models.Model):
    branch = models.CharField(max_length=20)
    vendor_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    # def __str__(self):
    #     return self.username
