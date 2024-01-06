from django.db.models import Q
import django_filters
from .models import User, Student


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
        self.filters["username"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "ID No."}
        )
        self.filters["name"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "Name"}
        )
        self.filters["email"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "Email"}
        )

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )


class StudentFilter(django_filters.FilterSet):
    student__username = django_filters.CharFilter(lookup_expr="exact", label="")
    student__name = django_filters.CharFilter(method="filter_by_name", label="")
    student__email = django_filters.CharFilter(lookup_expr="icontains", label="")
    program__title = django_filters.CharFilter(lookup_expr="icontains", label="")

    class Meta:
        model = Student
        fields = [
            "student__username",
            "student__name",
            "student__email",
            "program__title",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Change html classes and placeholders
        self.filters["student__username"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "ID No."}
        )
        self.filters["student__name"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "Name"}
        )
        self.filters["student__email"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "Email"}
        )
        self.filters["program__title"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "Program"}
        )

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            Q(student__first_name__icontains=value)
            | Q(student__last_name__icontains=value)
        )
