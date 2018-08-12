import os
from uuid import uuid4
from random import choice
from datetime import datetime
from itertools import product

from mimesis import Generic
from mimesis.enums import Gender
from mimesis.utils import download_image

from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Generate amount of fake users'

    def add_arguments(self, parser):
        parser.add_argument('count', default=10000, type=int, nargs='?')

    def handle(self, *args, **options):
        generics = [Generic('ru'), Generic('uk'), Generic('en')]
        genders = [Gender.MALE, Gender.FEMALE]
        variants = list(product(generics, genders))
        upload_to = User.avatar.field.upload_to
        # pathlib doesn't like trailing slash, so use os.path.join
        avatars_save_path = os.path.join(settings.BASE_DIR, upload_to)
        users_count = User.objects.count()
        for index in range(users_count, users_count + options['count']):
            generic, gender = choice(variants)
            user = User.objects.create_user(
                generic.person.email(),
                generic.person.name(gender=gender),
                generic.person.surname(gender=gender),
                f'password_{index + 1}',
                username=generic.person.identifier('id######@@'),
                birthday=datetime.strptime(
                    generic.datetime.date(start=1975, end=2000, fmt='%d.%m.%Y'),
                    '%d.%m.%Y'
                ),
                gender=gender.value.capitalize()[0],
                status=generic.text.quote(),
                avatar=os.path.join(
                    upload_to,
                    download_image(
                        url=f'{generic.internet.stock_image(width=300, height=300)}/{uuid4()}.jpg',  # noqa
                        save_path=avatars_save_path
                    )
                )
            )
            user.save()
