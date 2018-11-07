from datetime import datetime, timezone

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, View

from .forms import ProposalForm
from .models import Proposal


def is_cfp_open():
    return datetime.now(timezone.utc) <= settings.CFP_CLOSE_AT


def can_submit(request):
    if is_cfp_open():
        return  # We haven't hit the deadline yet, carry on

    bypass_token = request.GET.get("deadline-bypass-token", "")
    if bypass_token == settings.CFP_DEADLINE_BYPASS_TOKEN:
        return  # User has a valid deadline bypass token, carry on

    # CFP is closed, user cannot continue
    messages.error(request, "We're sorry, the Call For Proposals has closed")
    return redirect("home")


@method_decorator(login_required, name="dispatch")
class ConfirmAcceptance(View):
    def post(self, request, *args, **kwargs):
        # does the Proposal exist?
        try:
            proposal = Proposal.objects.get(self.kwargs["pk"])
        except Proposal.DoesNotExist:
            messages.error(request, "Unknown proposal")
            return redirect("home")

        # check the proposal is owned by the current user
        if request.user != proposal.author:
            messages.error(request, "Only a Proposal's owner can view it")
            return redirect("home")

        # has the proposal been confirmed?
        if proposal.state not in ["accept", "confirm"]:
            messages.success(
                request,
                "Unfortunately your proposal has not been accepted, and therefore cannot be confirmed.",
            )

        proposal.confirm_acceptance()

        messages.success(
            request,
            "Thank you for confirming you will be able to present your proposal. See you in Cardiff!",
        )

        return redirect(proposal.get_absolute_url())


@method_decorator(login_required, name="dispatch")
class ProposalDetail(DetailView):
    template_name = "proposal-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_cfp_open"] = is_cfp_open()
        return context

    def get_queryset(self):
        return Proposal.objects.filter(author=self.request.user).all()


@method_decorator(login_required, name="dispatch")
# @method_decorator(can_submit, name="dispatch")
class ProposalCreate(CreateView):
    form_class = ProposalForm
    template_name = "proposal-create.html"

    def form_valid(self, form):
        proposal = form.save(commit=False)
        proposal.author = self.request.user
        proposal.save()
        messages.success(self.request, "Thank you for submitting your proposal")
        # TODO: log this to slack?
        return redirect(proposal.get_absolute_url())


@method_decorator(login_required, name="dispatch")
# @method_decorator(can_submit, name="dispatch")
class ProposalEdit(UpdateView):
    form_class = ProposalForm
    template_name = "proposal-edit.html"

    def form_valid(self, form):
        proposal = form.save()
        messages.success(self.request, "Thank you for updating your proposal")
        return redirect(proposal.get_absolute_url())

    def get_queryset(self):
        return Proposal.objects.filter(author=self.request.user).all()
