from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404


class PropsoalManager(models.Manager):
    def get_by_proposal_id_or_404(self, proposal_id):
        id = self.model.id_scrambler.backward(proposal_id)
        return get_object_or_404(self.model, pk=id)

    def accepted_talks(self):
        return self.filter(Q(session_type="talk") & Q(state="accepted"))

    def reviewed_by_user(self, user):
        return self.accepted_talks().filter(vote__user=user).order_by("id")

    def unreviewed_by_user(self, user):
        return self.accepted_talks().exclude(vote__user=user).order_by("id")

    def of_interest_to_user(self, user):
        return (
            self.accepted_talks()
            .filter(vote__user=user, vote__is_interested=True)
            .order_by("id")
        )

    def not_of_interest_to_user(self, user):
        return (
            self.accepted_talks()
            .filter(vote__user=user, vote__is_interested=False)
            .order_by("id")
        )

    def get_random_unreviewed_by_user(self, user):
        return self.unreviewed_by_user(user).order_by("?").first()


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
