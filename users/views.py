from django.contrib.auth.models import User
from django.views.generic import DetailView


class UserDetail(DetailView):
    model = User
    context_object_name = 'user'
