from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from .forms import RegisterForm


class Register(CreateView):
    form_class = RegisterForm
    template_name = "register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "You are already signed in!")
            return redirect("home")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()  # Create the User

        # Log the User in for convenience
        user = authenticate(
            username=user.email, password=form.cleaned_data["password1"]
        )
        login(self.request, user)

        user.assign_a_snake()  # Give the User a snake

        return redirect(reverse("home"))
