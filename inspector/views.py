import functools
import operator

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView

from pyconuk.models import User


@method_decorator(staff_member_required, name="dispatch")
class SearchResults(TemplateView):
    searches = [
        {
            "model": User,
            "fields": ["email__icontains", "name__icontains"],
            "details_url": "inspector-user-detail",
        }
    ]
    template_name = "inspector/search-results.html"

    def get_results(self, query):
        results = []
        limit = 20
        for search_spec in self.searches:
            results = list(self.iter_search_model(search_spec, query, limit=limit + 1))
            name = search_spec["model"].__name__
            yield name, results

    def iter_search_model(self, search_spec, q, limit):
        """
        Query a model building filters from the search spec

        """
        model = search_spec["model"]
        fields = search_spec["fields"]
        query = model.objects.all()

        # Build and apply a Q based filter using fields from the search spec
        if q and fields:
            qfilter = functools.reduce(
                operator.or_, (Q(**{field: q}) for field in fields)
            )
            query = query.filter(qfilter)

        # Apply any excludes we might have
        exclude = search_spec.get("exclude")
        if exclude:
            query = query.exclude(exclude)

        query = query[:limit]
        for thing in query.iterator():
            # hack a URL reverse on
            thing.details_url = search_spec["details_url"]
            yield thing

    def get_context_data(self, **kwargs):
        query = self.request.GET.get("q")

        context = super().get_context_data(**kwargs)
        context["q"] = query
        context["results"] = dict(self.get_results(query)) if query else {}
        return context


@method_decorator(staff_member_required, name="dispatch")
class UserDetail(DetailView):
    model = User
    template_name = "inspector/user-detail.html"


@method_decorator(staff_member_required, name="dispatch")
class UserList(ListView):
    model = User
    template_name = "inspector/user-list.html"

    def get_ordering(self):
        ordering_kwarg = "ordering"
        order = self.request.GET.get(ordering_kwarg) or "name"
        return order
