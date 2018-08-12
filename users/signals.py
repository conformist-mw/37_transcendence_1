from itertools import count

from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User


@receiver(post_save, sender=User)
def add_username(sender, instance, created, **kwargs):  # noqa
    if created and not instance.username:
        user_fake_id_gen = count(User.objects.count())
        username = f'user_{next(user_fake_id_gen)}'
        while User.objects.filter(username=username).exists():
            username = f'user_{next(user_fake_id_gen)}'
        instance.username = username
        instance.save(update_fields=['username'])
