from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import Q, UniqueConstraint
from django.dispatch import receiver

# project import
from .utils import *
from core.models import ActivityLog

YEARS = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
)

# LEVEL_COURSE = "Level course"
BACHELOR_DEGREE = "Bachelor"
MASTER_DEGREE = "Master"

LEVEL = (
    # (LEVEL_COURSE, "Level course"),
    (BACHELOR_DEGREE, "Bachelor Degree"),
    (MASTER_DEGREE, "Master Degree"),
)

FIRST = "First"
SECOND = "Second"
THIRD = "Third"

SEMESTER = (
    (FIRST, "First"),
    (SECOND, "Second"),
    (THIRD, "Third"),
)


class ProgramManager(models.Manager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = Q(title__icontains=query) | Q(summary__icontains=query)
            queryset = queryset.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return queryset


class Program(models.Model):
    title = models.CharField(max_length=150, unique=True)
    summary = models.TextField(null=True, blank=True)

    objects = ProgramManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("program_detail", kwargs={"pk": self.pk})



@receiver(post_save, sender=Program)
def log_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=f"The program '{instance}' has been {verb}.")


@receiver(post_delete, sender=Program)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=f"The program '{instance}' has been deleted.")


class CourseManager(models.Manager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)
                | Q(summary__icontains=query)
                | Q(code__icontains=query)
                | Q(slug__icontains=query)
            )
            queryset = queryset.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return queryset


class Course(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    title = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=200, null=True)
    credit = models.IntegerField(null=True, default=0)
    summary = models.TextField(max_length=200, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
    year = models.IntegerField(choices=YEARS, default=0)
    semester = models.CharField(choices=SEMESTER, max_length=200)
    is_elective = models.BooleanField(default=False, blank=True, null=True)

    objects = CourseManager()

    def __str__(self):
        return "{0} ({1})".format(self.title, self.code)

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})

    @property
    def is_current_semester(self):
        from core.models import Semester

        current_semester = Semester.objects.get(is_current_semester=True)

        if self.semester == current_semester.semester:
            return True
        else:
            return False


def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(course_pre_save_receiver, sender=Course)


@receiver(post_save, sender=Course)
def log_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=f"The course '{instance}' has been {verb}.")


@receiver(post_delete, sender=Course)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=f"The course '{instance}' has been deleted.")


class CourseAllocation(models.Model):
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="allocated_lecturer",
    )
    courses = models.ManyToManyField(Course, related_name="allocated_course")
    session = models.ForeignKey(
        "core.Session", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.lecturer.get_full_name

    def get_absolute_url(self):
        return reverse("edit_allocated_course", kwargs={"pk": self.pk})
class CourseOffer(models.Model):
    """NOTE: Only department head can offer semester courses"""

    dep_head = models.ForeignKey("accounts.DepartmentHead", on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.dep_head)


class TimeSlot(models.Model):
    start_time = models.TimeField(unique = True, null = True)
    end_time = models.TimeField(unique = True, null = True)

    def clean(self):
        # Ensure end_time is later than start_time

        if self.end_time is None or self.start_time is None:
            raise ValidationError("Time slot cannot be empty")
        if self.end_time <= self.start_time:
            raise ValidationError(('End time must be later than start time.'))

        # Check for overlapping time slots
        overlapping_slots = TimeSlot.objects.filter(
            models.Q(start_time__lt=self.end_time) & models.Q(end_time__gt=self.start_time)
        ).exclude(pk=self.pk)  # Exclude self to allow updates to the same instance

        if overlapping_slots.exists():
            raise ValidationError(('This time slot overlaps with an existing time slot.'))
    def __str__(self):
        return f"Timeslot: {self.start_time} - {self.end_time}"


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    session = models.IntegerField(null = True)
    class_session = models.CharField(max_length=100, unique=True, blank = True, null = True)
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lecturer")

    def save(self, *args, **kwargs):
        if not self.class_session:
            self.class_session = f"{self.course.slug}-SS{self.session}"
        super(Class, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} - {self.class_session}"
    # def __str__(self):
    #     return f"{self.course.title} - {self.time_slot.time}"

    def get_absolute_url(self):
        return reverse("class_detail", kwargs={"pk": self.class_id})

    class Meta:
        constraints = [
            UniqueConstraint(fields=['session', 'course', 'time_slot'], name='unique_session_course_timeslot')
        ]

@receiver(post_save, sender=Class)
def log_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=f"The class for '{instance.course}' at '{instance.time_slot}' has been {verb}.")


@receiver(post_delete, sender=Class)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=f"The class for '{instance.course}' at '{instance.time_slot}' has been deleted.")

class Upload(models.Model):
    title = models.CharField(max_length=100)
    class_model = models.ForeignKey(Class, on_delete=models.CASCADE, null = True)
    file = models.FileField(
        upload_to="class_files/",
        help_text="Valid Files: pdf, docx, doc, xls, xlsx, ppt, pptx, zip, rar, 7zip",
        validators=[
            FileExtensionValidator(
                [
                    "pdf",
                    "docx",
                    "doc",
                    "xls",
                    "xlsx",
                    "ppt",
                    "pptx",
                    "zip",
                    "rar",
                    "7zip",
                    "txt"
                ]
            )
        ],
    )
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.file)[6:]

    def get_extension_short(self):
        ext = str(self.file).split(".")
        ext = ext[len(ext) - 1]

        if ext in ("doc", "docx"):
            return "word"
        elif ext == "pdf":
            return "pdf"
        elif ext in ("xls", "xlsx"):
            return "excel"
        elif ext in ("ppt", "pptx"):
            return "powerpoint"
        elif ext in ("zip", "rar", "7zip"):
            return "archive"

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


@receiver(post_save, sender=Upload)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"The file '{instance.title}' has been uploaded to the class '{instance.class_model.class_session}'."
        )
    else:
        ActivityLog.objects.create(
            message=f"The file '{instance.title}' of the class '{instance.class_model.class_session}' has been updated."
        )


@receiver(post_delete, sender=Upload)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The file '{instance.title}' of the class '{instance.class_model.class_session}' has been deleted."
    )


class UploadVideo(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    class_model = models.ForeignKey(Class, on_delete=models.CASCADE, null = True)
    video = models.FileField(
        upload_to="course_videos/",
        help_text="Valid video formats: mp4, mkv, wmv, 3gp, f4v, avi, mp3",
        validators=[
            FileExtensionValidator(["mp4", "mkv", "wmv", "3gp", "f4v", "avi", "mp3"])
        ],
    )
    summary = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse(
            "video_single", kwargs={"slug": self.class_model.class_session, "video_slug": self.slug}
        )

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)


def video_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(video_pre_save_receiver, sender=UploadVideo)


@receiver(post_save, sender=UploadVideo)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"The video '{instance.title}' has been uploaded to the class {instance.class_model.class_session}."
        )
    else:
        ActivityLog.objects.create(
            message=f"The video '{instance.title}' of the class '{instance.class_model.class_session}' has been updated."
        )


@receiver(post_delete, sender=UploadVideo)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The video '{instance.title}' of the class '{instance.class_model.class_session}' has been deleted."
    )



class Enrollment(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, null = True)
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="enrolled_class", null = True)
    course_enrolled = models.ForeignKey(Course, on_delete=models.CASCADE, related_name = "enrolled_course", null = True)
    retake = models.BooleanField(default=False)

    def __str__(self):
        return f"Student: {self.student}, Course: {self.course_enrolled}, Class: {self.class_enrolled}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['student', 'class_enrolled', 'course_enrolled'], name='unique_student_course_class')
        ]


@receiver(post_save, sender=Enrollment)
def log_enrollment_save(sender, instance, created, **kwargs):
    # Log the creation or update of the enrollment
    verb = "created" if created else "updated"
    ActivityLog.objects.create(
        message=f"Enrollment of student '{instance.student}' in course {instance.course_enrolled},"
                f" class '{instance.class_enrolled}' has been {verb}."
    )

    # Check for existing enrollments with the same course code
    if created:
        existing_enrollments = Enrollment.objects.filter(
            student=instance.student,
            course_enrolled__code=instance.course_enrolled.code
        ).exclude(pk=instance.pk)

        # If any existing enrollments are found, set retake to True
        if existing_enrollments.exists():
            instance.retake = True
            instance.save()

@receiver(post_delete, sender=Enrollment)
def log_enrollment_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"Enrollment of student '{instance.student}' in course {instance.course_enrolled},"
                f" class '{instance.class_enrolled}' has been deleted."
    )
