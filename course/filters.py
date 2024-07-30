from django.db.models import Q
import django_filters
from django.forms import Select
from django_filters import ModelChoiceFilter

from .models import Program, CourseAllocation, Course, Class, TimeSlot
from accounts.models import User


class ProgramFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains", label="")

    class Meta:
        model = Program
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Change html classes and placeholders
        self.filters["title"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "Program name"}
        )


class CourseAllocationFilter(django_filters.FilterSet):
    lecturer = django_filters.CharFilter(method="filter_by_lecturer", label="")
    course = django_filters.filters.CharFilter(method="filter_by_course", label="")

    class Meta:
        model = CourseAllocation
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Change html classes and placeholders
        self.filters["lecturer"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "Lecturer"}
        )
        self.filters["course"].field.widget.attrs.update(
            {"class": "au-input", "placeholder": "Course"}
        )

    def filter_by_lecturer(self, queryset, name, value):
        return queryset.filter(
            Q(lecturer__first_name__icontains=value)
            | Q(lecturer__last_name__icontains=value)
        )

    def filter_by_course(self, queryset, name, value):
        return queryset.filter(courses__title__icontains=value)


class ClassAllocationFilter(django_filters.FilterSet):
    lecturer = ModelChoiceFilter(
        queryset=User.objects.filter(id__in=Class.objects.values_list('lecturer', flat=True).distinct()),
        label="Select lecturer",
        widget=Select(attrs={'class': 'form-control'})
    )
    course = ModelChoiceFilter(
        queryset=Course.objects.filter(id__in=Class.objects.values_list('course', flat=True).distinct()),
        label="Select course",
        widget=Select(attrs={'class': 'form-control'})
    )
    time_slot = ModelChoiceFilter(
        queryset=TimeSlot.objects.filter(id__in=Class.objects.values_list('time_slot', flat=True).distinct()),
        label="Select time slot",
        widget=Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Class
        fields = ['lecturer', 'course', 'time_slot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Change HTML classes and placeholders if needed
        self.filters["lecturer"].field.widget.attrs.update(
            {"class": "form-control", "placeholder": "Lecturer"}
        )
        self.filters["course"].field.widget.attrs.update(
            {"class": "form-control", "placeholder": "Course"}
        )
        self.filters["time_slot"].field.widget.attrs.update(
            {"class": "form-control", "placeholder": "Time Slot"}
        )