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
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path(
        "favicon.png",
        RedirectView.as_view(
            url=staticfiles_storage.url("crown_black.svg"), permanent=False
        ),
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
    path(
        "diversity",
        TemplateView.as_view(template_name="diversity.html"),
        name="diversity",
    ),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
]

# Enable Debug Toolbar urls
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
