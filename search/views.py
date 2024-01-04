from itertools import chain
from django.views.generic import ListView
from core.models import NewsAndEvents
from course.models import Program, Course
from quiz.models import Quiz


class SearchView(ListView):
    template_name = "search/search_view.html"
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["count"] = self.count or 0
        context["query"] = self.request.GET.get("q")
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get("q", None)

        if query is not None:
            news_events_results = NewsAndEvents.objects.search(query)
            program_results = Program.objects.search(query)
            course_results = Course.objects.search(query)
            quiz_results = Quiz.objects.search(query)

            # combine querysets
            queryset_chain = chain(
                news_events_results, program_results, course_results, quiz_results
            )
            queryset = sorted(
                queryset_chain, key=lambda instance: instance.pk, reverse=True
            )
            self.count = len(queryset)  # since queryset is actually a list
            return queryset
        return NewsAndEvents.objects.none()  # just an empty queryset as default
