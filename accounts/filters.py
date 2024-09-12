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
    id_no = django_filters.CharFilter(
        field_name="student__username", lookup_expr="exact", label=""
    )
    name = django_filters.CharFilter(
        field_name="student__name", method="filter_by_name", label=""
    )
    email = django_filters.CharFilter(
        field_name="student__email", lookup_expr="icontains", label=""
    )
    program = django_filters.CharFilter(
        field_name="program__title", lookup_expr="icontains", label=""
    )

    class Meta:
        model = Student
        fields = [
            "id_no",
            "name",
            "email",
            "program",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Change html classes and placeholders
        self.filters["id_no"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "ID No."}
        )
        self.filters["name"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "Name"}
        )
        self.filters["email"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "Email"}
        )
        self.filters["program"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "Program"}
        )

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            Q(student__first_name__icontains=value)
            | Q(student__last_name__icontains=value)
        )
