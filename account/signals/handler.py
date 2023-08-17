from account.models import ClientProfile
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_client_profile(sender, instance, created, **kwargs):
    # If the instance is newly created and is_client is True
    if created and instance.is_client:
        ClientProfile.objects.create(client=instance, phone_number="", location="", shipping_location="", shipping_street="",)
