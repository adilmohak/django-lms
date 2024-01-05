from django.db.models import Q
import django_filters
from .models import User


class LecturerFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="exact", label="")
    name = django_filters.CharFilter(method="filter_by_name", label="")
    email = django_filters.CharFilter(lookup_expr="icontains", label="")

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Change html classes and placeholders
        self.filters["username"].field.widget.attrs.update({"class": "au-input"})
        self.filters["username"].field.widget.attrs.update({"placeholder": "ID No."})

        self.filters["name"].field.widget.attrs.update({"class": "au-input"})
        self.filters["name"].field.widget.attrs.update({"placeholder": "Name"})

        self.filters["email"].field.widget.attrs.update({"class": "au-input"})
        self.filters["email"].field.widget.attrs.update({"placeholder": "Email"})

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )
