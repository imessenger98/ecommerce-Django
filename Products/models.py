from django.db import models
from django.http.response import HttpResponse
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **other_fields):
        """
        Create and save a user with the given email and password. And any other fields, if specified.
        """
        if not email:
            raise ValueError('An Email address must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **other_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **other_fields):
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **other_fields)

    def create_superuser(self, email, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **other_fields)


class User(AbstractUser):
    STATUS = (
        ('admin', 'admin'),
        ('customer', 'customer'),
        ('driver', 'driver'),
    )
    username = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.IntegerField(null=True)
    role = models.CharField(max_length=30, null=True,
                            choices=STATUS, default="customer")
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.IntegerField(null=True, default=None)
    pic = models.ImageField(upload_to="images/", null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['address', 'phone', 'city', 'postcode']
    objects = UserManager()
    password = models.CharField(max_length=200, null=True)

    def get_username(self):
        return self.email


class order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Ordered', 'Ordered'),
        ('Accepted', 'Accepted'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Order Cancel', 'Order Cancel'),
        ('Customer Cancel', 'Customer Cancel'),
        ('Delivered', 'Delivered'),
        ('Added to Cart', 'Added to Cart'),
        ('Assigned to Driver', 'Assigned to Driver'),
    )
    order_date = models.DateField(null=True)
    customer_id = models.ForeignKey(
        'User', on_delete=models.CASCADE, null=True)
    vendor_id = models.ForeignKey(
        'Vendor.Vendors', on_delete=models.CASCADE, null=True)
    order_total = models. IntegerField(null=True)
    payment_method = models.CharField(default=" ", max_length=50, null=True)
    payment_status = models.BooleanField(default=" ", null=True)
    delivery_date = models.DateField(null=True)
    status = models.CharField(
        default="ordered", max_length=50, null=True, choices=STATUS)
    Is_delivered = models. BooleanField(default=False)

    def get_date(self):
        return self.delivery_date.date()


class orderdetails(models.Model):
    product_id = models.ForeignKey(
        'Commodity.Product', on_delete=models.CASCADE, null=True)
    product_qty = models.FloatField(null=True)
    product_price = models.IntegerField(null=True)
    subtotal = models.IntegerField(null=True)
    order = models.ForeignKey('order', on_delete=models.CASCADE, null=True)


class addtocart(models.Model):
    auser = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    aproduct = models.ForeignKey(
        'Commodity.Product', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True, default=1)


class dbwishlist(models.Model):
    wuser = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    wproduct = models.ForeignKey(
        'Commodity.Product', on_delete=models.CASCADE, null=True)
