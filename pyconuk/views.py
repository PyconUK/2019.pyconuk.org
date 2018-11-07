from datetime import datetime, timezone

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import ProfileForm, RegisterForm
from .models import User


class ProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = User
    template_name = "profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        # ticket = self.request.user.ticket
        # TODO: fix when tickets are implemented
        ticket = None
        context = super().get_context_data(**kwargs)

        context["ticket_rate"] = ticket.rate if ticket else ""
        context["badge_editing_closed"] = (
            datetime.now(timezone.utc) > settings.BADGE_EDITING_CLOSE_AT
        )

        return context

    def get_object(self, queryset=None):
        # TODO: prefetch_related tickets
        return self.request.user


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
