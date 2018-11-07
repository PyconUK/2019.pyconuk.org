from django.urls import path
from django.views.generic import TemplateView

from .views import SearchResults, UserDetail, UserList

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="inspector/home.html"),
        name="inspector-home",
    ),
    path("search", SearchResults.as_view(), name="inspector-search-results"),
    path("users", UserList.as_view(), name="inspector-user-list"),
    path("users/<pk>", UserDetail.as_view(), name="inspector-user-detail"),
]
