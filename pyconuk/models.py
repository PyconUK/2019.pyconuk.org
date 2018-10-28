import json
import os
import random

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    _user_has_module_perms,
    _user_has_perm,
)
from django.db import models
from django.utils import timezone

# https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations
with open(os.path.join(settings.BASE_DIR, "data", "countries.txt")) as f:
    countries = [line.strip() for line in f]
    COUNTRY_CHOICES = (
        [["not shared", "prefer not to say"]]
        + [[country, country] for country in countries]
        + [["other", "not listed here (please specify)"]]
    )


# https://en.wikipedia.org/wiki/List_of_adjectival_and_demonymic_forms_for_countries_and_nations
with open(os.path.join(settings.BASE_DIR, "data", "nationalities.txt")) as f:
    nationalities = (line.strip() for line in f)
    NATIONALITY_CHOICES = (
        [["not shared", "prefer not to say"]]
        + [[nationality, nationality] for nationality in nationalities]
        + [["other", "not listed here (please specify)"]]
    )


# https://www.ons.gov.uk/ons/guide-method/harmonisation/primary-set-of-harmonised-concepts-and-questions/ethnic-group.pdf
with open(os.path.join(settings.BASE_DIR, "data", "ethnicities.json")) as f:
    ethnicities = json.load(f)
    ETHNICITY_CHOICES = [["not shared", "prefer not to say"]] + [
        [ethnicity_category, [[ethnicity, ethnicity] for ethnicity in ethnicities]]
        for ethnicity_category, ethnicities in ethnicities
    ]

GENDER_CHOICES = [
    ["not shared", "prefer not to say"],
    ["female", "female"],
    ["male", "male"],
    ["other", "please specify"],
]

YEAR_OF_BIRTH_CHOICES = [["not shared", "prefer not to say"]] + [
    [str(year), str(year)] for year in range(1917, 2017)
]


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


class User(AbstractBaseUser, PermissionsMixin):
    email = models.TextField(
        null=False,
        unique=True,
        error_messages={"unique": "That email address has already been registered"},
    )
    password = models.TextField(null=True, blank=True)
    name = models.TextField(null=False, blank=False)

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    created_at = models.DateTimeField("date joined", default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    # Demographics
    year_of_birth = models.TextField(
        null=True, blank=True, choices=YEAR_OF_BIRTH_CHOICES
    )
    gender = models.TextField(null=True, blank=True, choices=GENDER_CHOICES)
    ethnicity = models.TextField(null=True, blank=True, choices=ETHNICITY_CHOICES)
    ethnicity_free_text = models.TextField(null=True, blank=True)
    nationality = models.TextField(null=True, blank=True, choices=NATIONALITY_CHOICES)
    country_of_residence = models.TextField(
        null=True, blank=True, choices=COUNTRY_CHOICES
    )
    dont_ask_demographics = models.BooleanField(default=False)

    # Requirements
    has_accessibility_reqs = models.NullBooleanField()
    accessibility_reqs = models.TextField(null=True, blank=True)
    has_childcare_reqs = models.NullBooleanField()
    childcare_reqs = models.TextField(null=True, blank=True)
    has_dietary_reqs = models.NullBooleanField()
    dietary_reqs = models.TextField(null=True, blank=True)

    # Extra responsibilities
    is_ukpa_member = models.NullBooleanField(null=True, blank=True)
    is_contributor = models.BooleanField(default=False)
    is_organiser = models.BooleanField(default=False)
    accepted_terms = models.DateTimeField(default=timezone.now)

    # Badge
    badge_company = models.TextField(blank=True, null=True)
    badge_twitter = models.TextField(blank=True, null=True)
    badge_pronoun = models.TextField(blank=True, null=True)
    badge_snake_colour = models.TextField(blank=True, null=True)
    badge_snake_extras = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

    @property
    def profile_complete(self):
        """
        Is a User's profile complete?

        Property which defines the criteria for a User's profile being
        in a state we consider complete.
        """
        # User has a ticket and is NOT a UKPA member
        if self.get_ticket() is not None and self.is_ukpa_member is None:
            return False

        # User has not completed 1 or more requirements questions
        requirements = [
            self.has_accessibility_reqs,
            self.has_childcare_reqs,
            self.has_dietary_reqs,
        ]
        if any(v is None for v in requirements):
            return False

        # skip the demographics checks
        if self.dont_ask_demographics:
            return True

        # All demographics questions have been answered
        return all(
            [
                self.year_of_birth,
                self.gender,
                self.ethnicity,
                self.nationality,
                self.country_of_residence,
            ]
        )

    def assign_a_snake(self):
        STANDARD_SNAKES = [
            ("blue", "deerstalker"),
            ("yellow", "crown"),
            ("red", "glasses"),
            ("green", "dragon"),
            ("purple", "mortar"),
            ("orange", "astronaut"),
        ]

        colour, extra = random.choice(STANDARD_SNAKES)

        self.badge_snake_colour = colour
        self.badge_snake_extras = extra

        self.save()

    def get_full_name(self):
        """This is used by the admin."""
        return self.name

    def get_short_name(self):
        """This is used by the admin."""
        return self.name

    def has_module_perms(self, module):
        return _user_has_module_perms(self, module)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)
