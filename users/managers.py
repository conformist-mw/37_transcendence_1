from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(
        self, email, first_name, last_name, password, **extra_fields
    ):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(
        self, email, first_name, last_name, password, **extra_fields
    ):
        return self._create_user(
            email, first_name, last_name, password, **extra_fields
        )

    def create_superuser(
        self, email, first_name, last_name, password, **extra_fields
    ):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(
            email, first_name, last_name, password, **extra_fields
        )
