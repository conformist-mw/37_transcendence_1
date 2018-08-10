from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import User


class UserDetail(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_detail.html'

    def get_object(self):
        if self.kwargs.get('pk'):
            return get_object_or_404(User, pk=self.kwargs['pk'])
        return get_object_or_404(User, username=self.kwargs['username'])

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        if kwargs.get('pk'):
            return HttpResponseRedirect(self.object.user_url)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
