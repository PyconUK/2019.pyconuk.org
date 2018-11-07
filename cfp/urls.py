from django.urls import path

from .views import ProposalCreate, ProposalDetail, ProposalEdit

urlpatterns = [
    path("new", ProposalCreate.as_view(), name="proposals-create"),
    path("<pk>", ProposalDetail.as_view(), name="proposals-detail"),
    path("<pk>/edit", ProposalEdit.as_view(), name="proposals-edit"),
]
