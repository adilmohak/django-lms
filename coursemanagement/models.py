from django.db import models
from course.models import Course
from accounts.models import DepartmentHead


class CourseOffer(models.Model):
	"""Only department head can offer a course"""
	dep_head = models.ForeignKey(DepartmentHead, on_delete=models.CASCADE)

	def __str__(self):
		return "{}".format(self.dep_head)


class CourseSetting(models.Model):
	add_drop = models.BooleanField(default=False)
