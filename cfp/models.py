from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone

from .choices import SESSION_TYPE_CHOICES, STATE_TYPE_CHOICES
from .validators import max_300_words


class Proposal(models.Model):
    author = models.ForeignKey(
        "pyconuk.User", related_name="proposals", on_delete=models.CASCADE
    )

    session_type = models.CharField(max_length=40, choices=SESSION_TYPE_CHOICES)
    title = models.CharField(max_length=60)
    subtitle = models.CharField(max_length=120, blank=True)
    copresenter_names = models.TextField(blank=True)
    description = models.TextField()
    description_private = models.TextField(validators=[max_300_words], blank=True)
    outline = models.TextField(blank=True)
    equipment = models.TextField(blank=True)
    aimed_at_new_programmers = models.BooleanField()
    aimed_at_teachers = models.BooleanField()
    aimed_at_data_scientists = models.BooleanField()
    would_like_mentor = models.BooleanField()
    would_like_longer_slot = models.BooleanField()
    state = models.CharField(max_length=40, blank=True, choices=STATE_TYPE_CHOICES)
    track = models.CharField(max_length=40, blank=True)
    special_reply_required = models.BooleanField(default=False)
    scheduled_room = models.CharField(max_length=40, blank=True)
    scheduled_time = models.DateTimeField(null=True)
    coc_conformity = models.BooleanField()
    ticket = models.BooleanField()
    confirmed = models.DateTimeField(null=True)
    replied_to = models.DateTimeField(null=True)

    break_event = models.BooleanField(default=False)
    conference_event = models.BooleanField(default=False)

    length_override = models.DurationField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.id})"

    @property
    def all_presenter_names(self):
        if self.copresenter_names:
            return f"{self.author.name}, {self.copresenter_names}"
        return self.author.name

    def confirm_acceptance(self):
        self.state = "confirm"
        self.confirmed = datetime.now()
        self.save()

    def full_title(self):
        return f"{self.title}: {self.subtitle}" if self.subtitle else self.title

    def get_absolute_url(self):
        return reverse("proposals-detail", kwargs={"pk": self.id})
