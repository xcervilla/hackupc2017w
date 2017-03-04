# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import base64

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from .models import User
from .forms import ValidateProfileForm


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', 'surname']

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserValidateProfileView(LoginRequiredMixin, FormView):
    form_class = ValidateProfileForm
    template_name = 'users/user_validate.html'

    def get_context_data(self, **kwargs):
        context = super(UserValidateProfileView, self).get_context_data(**kwargs)
        context['error'] = False
        if self.request.GET.get('error', 0) != 0:
            context['error'] = self.request.GET['error']
        context['user'] = User.objects.get(username=self.kwargs.get('username', None))
        return context

    def form_valid(self, form):
        result = self.request.user.validate_id(form.cleaned_data['frontal_photo'].read(),
                                               form.cleaned_data['back_photo'].read())
        if result is True:
            return HttpResponseRedirect(self.get_success_url())
        elif result == 'repeated':
            return HttpResponseRedirect(reverse('users:validate', args=[self.request.user.username])+'?error=repeated')
        return HttpResponseRedirect(reverse('users:validate', args=[self.request.user.username])+'?error=not_valid')

    def get_success_url(self):
        return self.request.user.get_absolute_url()
