from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserCreationForm
from users.models import User


def user_profile(request, user_id):
    if request.user.id == int(user_id):
        user = User.objects.get(id=user_id)
    else:
        raise PermissionDenied
    return render(request, 'user_profile.html',
                  {'user': user})


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('/')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
