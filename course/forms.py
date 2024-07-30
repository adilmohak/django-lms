from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from accounts.models import User
from .models import Program, Course, CourseAllocation, Upload, UploadVideo, TimeSlot, Class, Course


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TimeSlotForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Time Slot'))
        self.fields['start_time'].widgets = forms.TimeInput(format='%H:%M', attrs =
                                                            {'class': 'form-control',
                                                             'type': 'time',
                                                             'id': 'id_start_time'})
        self.fields['end_time'].widgets = forms.TimeInput(format='%H:%M', attrs = {'class': 'form-control',
                                                                   'type': 'time',
                                                                   'id' : 'id_end_time'})



class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["summary"].widget.attrs.update({"class": "form-control"})


class CourseAddForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["code"].widget.attrs.update({"class": "form-control"})
        # self.fields['courseUnit'].widget.attrs.update({'class': 'form-control'})
        self.fields["credit"].widget.attrs.update({"class": "form-control"})
        self.fields["summary"].widget.attrs.update({"class": "form-control"})
        self.fields["program"].widget.attrs.update({"class": "form-control"})
        self.fields["level"].widget.attrs.update({"class": "form-control"})
        self.fields["year"].widget.attrs.update({"class": "form-control"})
        self.fields["semester"].widget.attrs.update({"class": "form-control"})


class ClassAddForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all().order_by("level"),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select", "id": "id_course"}
        ),
        label="Course",
        required=True,
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        widget=forms.Select(attrs={"class": "browser-default custom-select", "id": "id_lecturer"}),
        label="lecturer",
        required=True,
    )
    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.all(),
        widget=forms.Select(attrs={"class": "browser-default custom-select", "id": "id_time_slot"}),
        label="timeslot",
        required=True,
    )

    class Meta:
        model = Class
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Class'))
        self.fields["session"].widget.attrs.update({"class": "form-control"})

        # if self.instance and self.instance.pk:
        #     course_id = self.instance.course.id
        #     self.fields['lecturer'].queryset = User.objects.filter(
        #         id__in=CourseAllocation.objects.filter(courses=course_id).values_list('lecturer_id', flat=True)
        #     )
        # else:
        #     self.fields['lecturer'].queryset = User.objects.none()

class EditClassAllocationForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all().order_by("level"),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select"}
        ),
        label="Course",
        required=True,
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        widget=forms.Select(attrs={"class": "browser-default custom-select"}),
        label="lecturer",
        required=True,
    )
    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.all(),
        widget=forms.Select(attrs={"class": "browser-default custom-select"}),
        label="timeslot",
        required=True,
    )

    class Meta:
        model = Class
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        #    user = kwargs.pop('user')
        super(EditClassAllocationForm, self).__init__(*args, **kwargs)
        self.fields["lecturer"].queryset = User.objects.filter(is_lecturer=True)

class CourseAllocationForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all().order_by("level"),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "browser-default checkbox"}
        ),
        required=True,
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        widget=forms.Select(attrs={"class": "browser-default custom-select"}),
        label="lecturer",
    )

    class Meta:
        model = CourseAllocation
        fields = ["lecturer", "courses"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(CourseAllocationForm, self).__init__(*args, **kwargs)
        self.fields["lecturer"].queryset = User.objects.filter(is_lecturer=True)


class EditCourseAllocationForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all().order_by("level"),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        widget=forms.Select(attrs={"class": "browser-default custom-select"}),
        label="lecturer",
    )

    class Meta:
        model = CourseAllocation
        fields = ["lecturer", "courses"]

    def __init__(self, *args, **kwargs):
        #    user = kwargs.pop('user')
        super(EditCourseAllocationForm, self).__init__(*args, **kwargs)
        self.fields["lecturer"].queryset = User.objects.filter(is_lecturer=True)


# Upload files to specific course
class UploadFormFile(forms.ModelForm):
    class Meta:
        model = Upload
        fields = (
            "title",
            "file",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["file"].widget.attrs.update({"class": "form-control"})


# Upload video to specific course
class UploadFormVideo(forms.ModelForm):
    class Meta:
        model = UploadVideo
        fields = (
            "title",
            "video",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["video"].widget.attrs.update({"class": "form-control"})
