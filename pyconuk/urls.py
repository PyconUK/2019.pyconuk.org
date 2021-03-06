"""pyconuk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

from .views import ProfileEdit, Register

urlpatterns = [
    path(
        "favicon.png",
        RedirectView.as_view(
            url=staticfiles_storage.url("crown_black.svg"), permanent=False
        ),
    ),
    path(
        "call-for-proposals",
        TemplateView.as_view(template_name="cfp/call-for-proposals.html"),
        name="call-for-proposals",
    ),
    path("coc", TemplateView.as_view(template_name="coc.html"), name="coc"),
    path(
        "coc/reporting-guidelines",
        TemplateView.as_view(template_name="coc_reporting_guidelines.html"),
        name="coc-reporting-guidelines",
    ),
    path(
        "coc/incident-handling-guidelines",
        TemplateView.as_view(template_name="coc_handling_guidelines.html"),
        name="coc-handling-guidelines",
    ),
    path("contact", TemplateView.as_view(template_name="contact.html"), name="contact"),
    path(
        "diversity",
        TemplateView.as_view(template_name="diversity.html"),
        name="diversity",
    ),
    path("inspector/", include("inspector.urls")),
    path(
        "financial-assistance",
        TemplateView.as_view(template_name="fin_aid.html"),
        name="fin-aid",
    ),
    path("legal", TemplateView.as_view(template_name="legal.html"), name="legal"),
    path(
        "profile",
        login_required(TemplateView.as_view(template_name="profile.html")),
        name="profile",
    ),
    path("profile/edit", ProfileEdit.as_view(), name="profile-edit"),
    path("proposals/", include("cfp.urls")),
    path(
        "schedule", TemplateView.as_view(template_name="schedule.html"), name="schedule"
    ),
    path(
        "sponsorship",
        TemplateView.as_view(template_name="sponsorship.html"),
        name="sponsorship",
    ),
    path(
        "sponsorship/sponsor-information",
        TemplateView.as_view(template_name="sponsor-information.html"),
        name="sponsor-information",
    ),
    path(
        "sponsorship/our-sponsors",
        TemplateView.as_view(template_name="our-sponsors.html"),
        name="our-sponsors",
    ),
    path(
        "travel-and-accommodation",
        TemplateView.as_view(template_name="travel-and-accommodation.html"),
        name="travel-and-accommodation",
    ),
    path(
        "travel-and-accommodation/travel",
        TemplateView.as_view(template_name="travel.html"),
        name="travel",
    ),
    # path(
    #     "travel-and-accommodation/accommodation",
    #     TemplateView.as_view(template_name="accommodation.html"),
    #     name="accommodation",
    # ),
    path("venue", TemplateView.as_view(template_name="venue.html"), name="venue"),
    path("register", Register.as_view(), name="register"),
    path("", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
]

# Enable Debug Toolbar urls
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
