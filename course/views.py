from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Avg, Max, Min, Count
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django_filters.views import FilterView

from accounts.models import User, Student
from core.models import Session, Semester
from result.models import TakenCourse
from accounts.decorators import lecturer_required, student_required, admin_required
from .forms import (
    ProgramForm,
    CourseAddForm,
    CourseAllocationForm,
    EditCourseAllocationForm,
    UploadFormFile,
    UploadFormVideo,
    TimeSlotForm,
    ClassAddForm,
    EditClassAllocationForm
)
from .filters import ProgramFilter, CourseAllocationFilter, ClassAllocationFilter
from .models import Program, Course, CourseAllocation, Upload, UploadVideo, Class, Enrollment


@method_decorator([login_required], name="dispatch")
class ProgramFilterView(FilterView):
    filterset_class = ProgramFilter
    template_name = "course/program_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Programs"
        return context

@login_required
@admin_required
def add_timeslot(request):
    if request.method == "POST":
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Time slot at " + request.POST.get("start_time") + "-" + request.POST.get("end_time") + "added!"
            )
            return redirect("add_timeslot")
        else:
            messages.error(request, "")
    else:
        form = TimeSlotForm()

    return render(
        request,
        "course/add_timeslot.html",
        {
            "form": form,
            "title": "Add Timeslot"
        }
    )

@login_required
@lecturer_required
def program_add(request):
    if request.method == "POST":
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, request.POST.get("title") + " program has been created."
            )
            return redirect("programs")
        else:
            messages.error(request, "Correct the error(S) below.")
    else:
        form = ProgramForm()

    return render(
        request,
        "course/program_add.html",
        {
            "title": "Add Program",
            "form": form,
        },
    )


@login_required
def program_detail(request, pk):
    program = Program.objects.get(pk=pk)

    if request.user.is_lecturer:
        course_allocations = CourseAllocation.objects.filter(lecturer_id=request.user.id)
        course_ids = course_allocations.values_list('courses', flat=True).distinct()
        courses = Course.objects.filter(program_id=pk, id__in=course_ids).order_by("-year")
    elif request.user.is_student:
        student_ids = Student.objects.filter(student_id=request.user.id).values_list('id', flat=True).distinct()
        course_allocations = Enrollment.objects.filter(student_id__in= student_ids)
        course_ids = course_allocations.values_list('course_enrolled_id', flat=True).distinct()
        # print(course_allocations, request.user.id)
        courses = Course.objects.filter(program_id=pk, id__in=course_ids).order_by("-year")
    else:
        courses = Course.objects.filter(program_id=pk).order_by("-year")

    # courses = Course.objects.filter(program_id=pk).order_by("-year")
    credits = Course.objects.aggregate(Sum("credit"))

    paginator = Paginator(courses, 10)
    page = request.GET.get("page")

    courses = paginator.get_page(page)

    return render(
        request,
        "course/program_single.html",
        {
            "title": program.title,
            "program": program,
            "courses": courses,
            "credits": credits,
        },
    )


@login_required
@lecturer_required
def program_edit(request, pk):
    program = Program.objects.get(pk=pk)

    if request.method == "POST":
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(
                request, str(request.POST.get("title")) + " program has been updated."
            )
            return redirect("programs")
    else:
        form = ProgramForm(instance=program)

    return render(
        request,
        "course/program_add.html",
        {"title": "Edit Program", "form": form},
    )


@login_required
@lecturer_required
def program_delete(request, pk):
    program = Program.objects.get(pk=pk)
    title = program.title
    program.delete()
    messages.success(request, "Program " + title + " has been deleted.")

    return redirect("programs")


# ########################################################


# ########################################################
# Course views
# ########################################################
@login_required
def course_single(request, slug):
    course = Course.objects.get(slug=slug)
    if request.user.is_lecturer:
        class_allocations = Class.objects.filter(lecturer_id=request.user.id)
        class_ids = class_allocations.values_list('class_id', flat=True).distinct()
        classes = Class.objects.filter(course_id=course.id, class_id__in = class_ids).order_by("-session")
    elif request.user.is_student:
        student_ids = Student.objects.filter(student_id=request.user.id).values_list('id', flat=True).distinct()
        class_allocations = Enrollment.objects.filter(student_id__in=student_ids)
        class_ids = class_allocations.values_list('class_enrolled_id', flat=True).distinct()
        classes = Class.objects.filter(course_id=course.id, class_id__in=class_ids).order_by("-session")
    else:
        classes = Class.objects.filter(course_id=course.id).order_by("-session")

    lecturer_ids = classes.values_list('lecturer', flat=True).distinct()
    lecturers = User.objects.filter(id__in=lecturer_ids)

    return render(
        request,
        "course/course_single.html",
        {
            "title": course.title,
            "course": course,
            "classes": classes,
            "lecturers": lecturers,
            "media_url": settings.MEDIA_ROOT,
        },
    )


@login_required
@lecturer_required
def course_add(request, pk):
    users = User.objects.all()
    if request.method == "POST":
        form = CourseAddForm(request.POST)
        course_name = request.POST.get("title")
        course_code = request.POST.get("code")
        if form.is_valid():
            form.save()
            messages.success(
                request, (course_name + "(" + course_code + ")" + " has been created.")
            )
            return redirect("program_detail", pk=request.POST.get("program"))
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = CourseAddForm(initial={"program": Program.objects.get(pk=pk)})

    return render(
        request,
        "course/course_add.html",
        {
            "title": "Add Course",
            "form": form,
            "program": pk,
            "users": users,
        },
    )


@login_required
@lecturer_required
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == "POST":
        form = CourseAddForm(request.POST, instance=course)
        course_name = request.POST.get("title")
        course_code = request.POST.get("code")
        if form.is_valid():
            form.save()
            messages.success(
                request, (course_name + "(" + course_code + ")" + " has been updated.")
            )
            return redirect("program_detail", pk=request.POST.get("program"))
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = CourseAddForm(instance=course)

    return render(
        request,
        "course/course_add.html",
        {
            "title": "Edit Course",
            # 'form': form, 'program': pk, 'course': pk
            "form": form,
        },
    )


@login_required
@lecturer_required
def course_delete(request, slug):
    course = Course.objects.get(slug=slug)
    # course_name = course.title
    course.delete()
    messages.success(request, "Course " + course.title + " has been deleted.")

    return redirect("program_detail", pk=course.program.id)



##########################################################

##########################################################
# Class Allocation
##########################################################

def get_lecturers_by_course(request, course_id):
    lecturers = User.objects.filter(
        id__in=CourseAllocation.objects.filter(courses=course_id).values_list('lecturer_id', flat=True)
    )
    lecturers_data = [{'id': lecturer.id, 'name': lecturer.get_full_name()} for lecturer in lecturers]
    return JsonResponse({'lecturers': lecturers_data})
@method_decorator([admin_required], name="dispatch")
class ClassAddView(CreateView):
    # model = Class
    form_class = ClassAddForm
    template_name = 'course/class_allocation_form.html'
    # success_url = reverse_lazy('class_list')  # Redirect to the class list view after successful form submission
    # success_message = "Class added successfully!"

    def form_valid(self, form):
        form.save()
        return redirect("class_list")

    # def get_form_kwargs(self):
    #     kwargs = super(CourseAllocationFormView, self).get_form_kwargs()
    #     kwargs["user"] = self.request.user
    #     return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Assign Class"
        return context

@method_decorator([login_required], name="dispatch")
class ClassAllocationFilterView(FilterView):
    filterset_class = ClassAllocationFilter
    template_name = "course/class_allocation_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Class Allocations"
        return context


def class_add(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = ClassAddForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.course = course
            new_class.save()
            messages.success(
                request, f"Class for {course.title} has been created."
            )
            return redirect("course_detail", slug=course.slug)
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = ClassAddForm(initial={'course': course})
    return render(
        request,
        "course/class_allocation_form.html",
        {
            "title": "Add Class",
            "form": form,
            "course": course,
        },
    )

@login_required
@lecturer_required
def edit_allocated_class(request, pk):
    allocated = get_object_or_404(Class, pk=pk)
    if request.method == "POST":
        form = EditClassAllocationForm(request.POST, instance=allocated)
        if form.is_valid():
            form.save()
            messages.success(request, "Class assigned has been updated.")
            return redirect("class_list")
    else:
        form = EditClassAllocationForm(instance=allocated)

    return render(
        request,
        "course/class_allocation_form.html",
        {"title": "Edit Course Allocated", "form": form, "allocated": pk},
    )


@login_required
@lecturer_required
def deallocate_class(request, pk):
    classes = Class.objects.get(pk=pk)
    classes.delete()
    messages.success(request, "successfully deallocate!")
    return redirect("class_list")

def class_single(request, pk):
    class_instance = Class.objects.get(class_id=pk)
    files = Upload.objects.filter(class_model = class_instance)
    videos = UploadVideo.objects.filter(class_model = class_instance)

    # lecturers = User.objects.filter(allocated_lecturer__pk=course.id)
    lecturers = User.objects.filter(id=class_instance.lecturer.id)

    return render(
        request,
        "course/class_single.html",
        {
            "title": f"Class Details: {class_instance.class_session}",
            "class": class_instance,
            "files": files,
            "videos": videos,
            "lecturers": lecturers,
            "media_url": settings.MEDIA_URL,
        },
    )

# @login_required
# def course_detail(request, pk):
#     courses = Course.objects.get(pk=pk)
#     classes = Class.objects.filter(course_id=pk).order_by("-time_slot")
#     # time_slot = Class.objects.aggregate(Sum("credit"))
#
#     paginator = Paginator(classes, 10)
#     page = request.GET.get("page")
#
#     classes = paginator.get_page(page)
#
#     return render(
#         request,
#         "course/class_single.html",
#         {
#             "title": courses.title,
#             "course": courses,
#             "class": classes,
#             # "credits": credits,
#         },
#     )

# ########################################################


# ########################################################
# Course Allocation
# ########################################################
@method_decorator([login_required], name="dispatch")
class CourseAllocationFormView(CreateView):
    form_class = CourseAllocationForm
    template_name = "course/course_allocation_form.html"

    def get_form_kwargs(self):
        kwargs = super(CourseAllocationFormView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        # if a staff has been allocated a course before update it else create new
        lecturer = form.cleaned_data["lecturer"]
        selected_courses = form.cleaned_data["courses"]
        courses = ()
        for course in selected_courses:
            courses += (course.pk,)
        # print(courses)

        try:
            a = CourseAllocation.objects.get(lecturer=lecturer)
        except:
            a = CourseAllocation.objects.create(lecturer=lecturer)
        for i in range(0, selected_courses.count()):
            a.courses.add(courses[i])
            a.save()
        return redirect("course_allocation_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Assign Course"
        return context


@method_decorator([login_required], name="dispatch")
class CourseAllocationFilterView(FilterView):
    filterset_class = CourseAllocationFilter
    template_name = "course/course_allocation_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Course Allocations"
        return context


@login_required
@lecturer_required
def edit_allocated_course(request, pk):
    allocated = get_object_or_404(CourseAllocation, pk=pk)
    if request.method == "POST":
        form = EditCourseAllocationForm(request.POST, instance=allocated)
        if form.is_valid():
            form.save()
            messages.success(request, "course assigned has been updated.")
            return redirect("course_allocation_view")
    else:
        form = EditCourseAllocationForm(instance=allocated)

    return render(
        request,
        "course/course_allocation_form.html",
        {"title": "Edit Course Allocated", "form": form, "allocated": pk},
    )


@login_required
@lecturer_required
def deallocate_course(request, pk):
    course = CourseAllocation.objects.get(pk=pk)
    course.delete()
    messages.success(request, "successfully deallocate!")
    return redirect("course_allocation_view")


# ########################################################


# ########################################################
# File Upload views
# ########################################################
@login_required
@lecturer_required
def handle_file_upload(request, pk):
    class_instance = Class.objects.get(class_id=pk)
    course = class_instance.course  # Make sure course is correctly fetched
    program = course.program  # Make sure program is correctly fetched
    if request.method == "POST":
        form = UploadFormFile(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.class_model = class_instance
            obj.save()

            messages.success(
                request, (request.POST.get("title") + " has been uploaded.")
            )
            return redirect("class_detail", pk=pk)
    else:
        form = UploadFormFile()
    return render(
        request,
        "upload/upload_file_form.html",
        {"title": "File Upload", "form": form, "class_instance": class_instance},
    )


@login_required
@lecturer_required
def handle_file_edit(request, pk, file_id):
    class_instance = Class.objects.get(class_id=pk)
    instance = Upload.objects.get(pk=file_id)
    if request.method == "POST":
        form = UploadFormFile(request.POST, request.FILES, instance=instance)
        # file_name = request.POST.get('name')
        if form.is_valid():
            form.save()
            messages.success(
                request, (request.POST.get("title") + " has been updated.")
            )
            return redirect("class_detail", pk = pk)
    else:
        form = UploadFormFile(instance=instance)

    return render(
        request,
        "upload/upload_file_form.html",
        {"title": instance.title, "form": form, "class_instance": class_instance},
    )


def handle_file_delete(request, pk, file_id):
    file = Upload.objects.get(pk=file_id)
    # file_name = file.name
    file.delete()

    messages.success(request, (file.title + " has been deleted."))
    return redirect("class_detail", pk=pk)


# ########################################################
# Video Upload views
# ########################################################
@login_required
@lecturer_required
def handle_video_upload(request, pk):
    class_instance = get_object_or_404(Class, class_id=pk)
    course = class_instance.course  # Make sure course is correctly fetched
    program = course.program  # Make sure program is correctly fetched
    if request.method == "POST":
        form = UploadFormVideo(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.class_model = class_instance
            obj.save()

            messages.success(
                request, (request.POST.get("title") + " has been uploaded.")
            )
            return redirect("class_detail", pk=pk)
    else:
        form = UploadFormVideo()
    return render(
        request,
        "upload/upload_video_form.html",
        {"title": "Video Upload", "form": form, "class": class_instance},
    )


@login_required
# @lecturer_required
def handle_video_single(request, pk, video_slug):
    class_instance = get_object_or_404(Class, class_id = pk)
    video = get_object_or_404(UploadVideo, slug=video_slug)
    return render(request, "upload/video_single.html", {"video": video})


@login_required
@lecturer_required
def handle_video_edit(request, pk, video_slug):
    course = Class.objects.get(class_id = pk)
    instance = UploadVideo.objects.get(slug=video_slug)
    if request.method == "POST":
        form = UploadFormVideo(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(
                request, (request.POST.get("title") + " has been updated.")
            )
            return redirect("class_detail", pk = pk)
    else:
        form = UploadFormVideo(instance=instance)

    return render(
        request,
        "upload/upload_video_form.html",
        {"title": instance.title, "form": form, "course": course},
    )


def handle_video_delete(request, pk, video_slug):
    video = get_object_or_404(UploadVideo, slug=video_slug)
    # video = UploadVideo.objects.get(slug=video_slug)
    video.delete()

    messages.success(request, (video.title + " has been deleted."))
    return redirect("class_detail", pk = pk)


# ########################################################


# ########################################################
# Course Registration
# ########################################################
@login_required
@student_required
def course_registration(request):
    if request.method == "POST":
        student = Student.objects.get(student__pk=request.user.id)
        ids = ()
        data = request.POST.copy()
        data.pop("csrfmiddlewaretoken", None)  # remove csrf_token
        # Extract course and class information
        courses_selected = []
        classes_selected = {}
        for key, value in data.items():
            print(f"Processing {key}: {value}")
            if key.startswith("course_"):
                course_id = key.split("_")[1]
                course = Course.objects.get(pk=course_id)
                # Check if a class was selected for this course
                class_key = f"class_{course_id}"
                if class_key in data and data[class_key]:
                    selected_class = Class.objects.get(pk=data[class_key])
                    classes_selected[course_id] = selected_class
                else:
                    classes_selected[course_id] = None

                # Create enrollment record
                if course_id not in courses_selected:
                    courses_selected.append(course_id)
                    enroll = Enrollment.objects.create(
                        student=student,
                        course_enrolled=course,
                        class_enrolled=classes_selected[course_id]
                    )
                    takencourse = TakenCourse.objects.create(student=student, course=course)
                    enroll.save()
                    takencourse.save()


        messages.success(request, "Courses and classes registered successfully!")
        return redirect("course_registration")
    else:
        current_semester = Semester.objects.filter(is_current_semester=True).first()
        if not current_semester:
            messages.error(request, "No active semester found.")
            return render(request, "course/course_registration.html")

        # student = Student.objects.get(student__pk=request.user.id)
        student = get_object_or_404(Student, student__id=request.user.id)
        taken_courses = TakenCourse.objects.filter(student__student__id=request.user.id)
        t = ()
        for i in taken_courses:
            t += (i.course.pk,)

        courses = (
            Course.objects.filter(
                program__pk=student.program.id,
                level=student.level,
                semester=current_semester,
            )
            .exclude(id__in=t)
            .order_by("year")
        )
        # Extract course IDs from the queryset
        course_ids = courses.values_list('id', flat=True)

        # Query all classes related to the courses
        classes = Class.objects.filter(course__in=course_ids)

        all_courses = Course.objects.filter(
            level=student.level, program__pk=student.program.id
        )

        no_course_is_registered = False  # Check if no course is registered
        all_courses_are_registered = False

        registered_courses = Course.objects.filter(level=student.level).filter(id__in=t)
        if (
            registered_courses.count() == 0
        ):  # Check if number of registered courses is 0
            no_course_is_registered = True

        if registered_courses.count() == all_courses.count():
            all_courses_are_registered = True

        total_first_semester_credit = 0
        total_sec_semester_credit = 0
        total_registered_credit = 0
        for i in courses:
            if i.semester == "First":
                total_first_semester_credit += int(i.credit)
            if i.semester == "Second":
                total_sec_semester_credit += int(i.credit)
        for i in registered_courses:
            total_registered_credit += int(i.credit)
        context = {
            "is_calender_on": True,
            "all_courses_are_registered": all_courses_are_registered,
            "no_course_is_registered": no_course_is_registered,
            "current_semester": current_semester,
            "courses": courses,
            "total_first_semester_credit": total_first_semester_credit,
            "total_sec_semester_credit": total_sec_semester_credit,
            "registered_courses": registered_courses,
            "total_registered_credit": total_registered_credit,
            "student": student,
            "classes": classes,
        }
        print(no_course_is_registered)
        return render(request, "course/course_registration.html", context)


@login_required
@student_required
def course_drop(request):
    if request.method == "POST":
        student = Student.objects.get(student__pk=request.user.id)
        ids = ()
        data = request.POST.copy()
        data.pop("csrfmiddlewaretoken", None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            course = Course.objects.get(pk=ids[s])
            obj = TakenCourse.objects.get(student=student, course=course)
            obj.delete()
        messages.success(request, "Successfully Dropped!")
        return redirect("course_registration")


# ########################################################


@login_required
def user_course_list(request):
    if request.user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id)

        return render(request, "course/user_course_list.html", {"courses": courses})

    elif request.user.is_student:
        student = Student.objects.get(student__pk=request.user.id)
        taken_courses = TakenCourse.objects.filter(
            student__student__id=student.student.id
        )
        courses = Course.objects.filter(level=student.level).filter(
            program__pk=student.program.id
        )

        return render(
            request,
            "course/user_course_list.html",
            {"student": student, "taken_courses": taken_courses, "courses": courses},
        )

    else:
        return render(request, "course/user_course_list.html")