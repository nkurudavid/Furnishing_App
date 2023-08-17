from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from . manager import UserManager


# Create your models here.
class User(AbstractUser):
    class Gender(models.TextChoices):
        SELECT = "", "Select Gender"
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    first_name = models.CharField(verbose_name="First Name", max_length=50, blank=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, blank=False)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True, blank=False)
    gender = models.CharField(verbose_name="Gender", choices=Gender.choices, default=Gender.SELECT, max_length=10)
    is_manager = models.BooleanField(verbose_name="Is Manger", default=False)
    is_client = models.BooleanField(verbose_name="Is Client", default=False)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    # update django about user model
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)



class ClientProfile(models.Model):
    client = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="client_profile", verbose_name="Client", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(verbose_name = "Phone Number", blank=True, unique=True)
    location = models.CharField(verbose_name="Location", max_length=100, blank=True, null=True)
    shipping_location = models.CharField(verbose_name="Shipping Location", max_length=100, blank=True, null=True)
    shipping_street = models.CharField(verbose_name="Shipping Street", max_length=50, blank=True, null=True)
    def __str__(self):
        return "{} {}".format(self.client.first_name, self.client.last_name)