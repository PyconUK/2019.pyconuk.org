from django.core.exceptions import ValidationError


def max_300_words(value):
    num_words = len(value.split())
    if num_words > 300:
        raise ValidationError(f"Field is too long: {num_words} words / 300 words limit")
