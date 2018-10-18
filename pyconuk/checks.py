from django.conf import settings
from django.core.checks import Error


ENVVAR_WATCHED = ["SECRET_KEY"]


def env_vars_check(app_configs, **kwargs):
    """
    Ensure critical env vars are set in production.
    """
    errors = []
    for watched in ENVVAR_WATCHED:
        if getattr(settings, watched) == settings.ENVVAR_SENTINAL:
            msg = f"Env var '{watched}' must be set in production."
            errors.append(Error(msg))
    return errors
