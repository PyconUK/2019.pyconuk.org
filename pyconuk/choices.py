import os
import json
from django.conf import settings

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
