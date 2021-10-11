from django.db import models
from course.models import Course
from accounts.models import DepHead


class CourseOffer(models.Model):
	dep_head = models.ForeignKey(DepHead, on_delete=models.CASCADE)

	def __str__(self):
		return "{}".format(self.dep_head)
