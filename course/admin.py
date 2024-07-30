from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Program, Course, CourseAllocation, Upload, TimeSlot, Enrollment, Class


admin.site.register(Program)
admin.site.register(Course)
admin.site.register(CourseAllocation)
admin.site.register(Upload)
admin.site.register(TimeSlot)
admin.site.register(Enrollment)
admin.site.register(Class)
