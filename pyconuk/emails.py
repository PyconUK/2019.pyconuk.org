from functools import partial

from django.conf import settings
from incuna_mail import send

send_mail = partial(
    send,
    reply_to="PyCon UK 2019 <pyconuk@uk.python.org>",
    sender=f"PyCon UK 2019 <noreply@{settings.ALLOWED_HOSTS[0]}>",
)
