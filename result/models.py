from django.db import models
from django.urls import reverse

from accounts.models import Student
from app.models import Session, Semester
from course.models import Course

YEARS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (4, '5'),
        (4, '6'),
    )

# LEVEL_COURSE = "Level course"
BACHLOAR_DEGREE = "Bachloar"
MASTER_DEGREE = "Master"

LEVEL = (
    # (LEVEL_COURSE, "Level course"),
    (BACHLOAR_DEGREE, "Bachloar Degree"),
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

A_plus = "A+"
A = "A"
A_minus = "A-"
B_plus = "B+"
B = "B"
B_minus = "B-"
C_plus = "C+"
C = "C"
C_minus = "C-"
D = "D"
F = "F"
NG = "NG"

GRADE = (
        (A_plus, "A+"),
        (A, "A"),
        (A_minus, "A-"),
        (B_plus, "B+"),
        (B, "B"),
        (B_minus, "B-"),
        (C_plus, "C+"),
        (C, "C"),
        (C_minus, "C-"),
        (D, "D"),
        (F, "F"),
        (NG, "NG"),
)

PASS = "PASS"
FAIL = "FAIL"

COMMENT = (
    (PASS, "PASS"),
    (FAIL, "FAIL"),
)


class TakenCourseManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)


class TakenCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='taken_courses')
    assignment = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    mid_exam = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    quiz = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    attendance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    final_exam = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    grade = models.CharField(choices=GRADE, max_length=2, blank=True)
    point = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    comment = models.CharField(choices=COMMENT, max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.course.slug})

    def __str__(self):
        return "{0} ({1})".format(self.course.title, self.course.code)

    # @staticmethod
    def get_total(self, assignment, mid_exam, quiz, attendance, final_exam):
        return float(assignment) + float(mid_exam) + float(quiz) + float(attendance) + float(final_exam) 

    # @staticmethod
    def get_grade(self, total):
        # total = float(assignment) + float(mid_exam) + float(quiz) + float(attendance) + float(final_exam)
        # total = self.get_total(assignment=assignment, mid_exam=mid_exam, quiz=quiz, attendance=attendance, final_exam=final_exam)
        # total = total
        if total >= 90:
            grade = A_plus
        elif total >= 85:
            grade = A
        elif total >= 80:
            grade = A_minus
        elif total >= 75:
            grade = B_plus
        elif total >= 70:
            grade = B
        elif total >= 65:
            grade = B_minus
        elif total >= 60:
            grade = C_plus
        elif total >= 55:
            grade = C
        elif total >= 50:
            grade = C_minus
        elif total >= 45:
            grade = D
        elif total < 45:
            grade = F
        else:
            grade = NG
        return grade

    # @staticmethod
    def get_comment(self, grade):
        if grade == F or grade == NG:
            comment = FAIL
        # elif grade == NG:
        #     comment = FAIL
        else:
            comment = PASS
        return comment

    def get_point(self, grade):
        p = 0
        # point = 0
        # for i in student:
        credit = self.course.credit
        if self.grade == A_plus:
            point = 4
        elif self.grade == A:
            point = 4
        elif self.grade == A_minus:
            point = 3.75
        elif self.grade == B_plus:
            point = 3.5
        elif self.grade == B:
            point = 3
        elif self.grade == B_minus:
            point = 2.75
        elif self.grade == C_plus:
            point = 2.5
        elif self.grade == C:
            point = 2
        elif self.grade == C_minus:
            point = 1.75
        elif self.grade == D:
            point = 1
        else:
            point = 0
        p += int(credit) * point
        return p

    def calculate_gpa(self, total_credit_in_semester):
        current_semester = Semester.objects.get(is_current_semester=True)
        student = TakenCourse.objects.filter(student=self.student, course__level=self.student.level, course__semester=current_semester)
        p = 0
        point = 0
        for i in student:
            credit = i.course.credit
            if i.grade == A_plus:
                point = 4
            elif i.grade == A:
                point = 4
            elif i.grade == A_minus:
                point = 3.75
            elif i.grade == B_plus:
                point = 3.5
            elif i.grade == B:
                point = 3
            elif i.grade == B_minus:
                point = 2.75
            elif i.grade == C_plus:
                point = 2.5
            elif i.grade == C:
                point = 2
            elif i.grade == C_minus:
                point = 1.75
            elif i.grade == D:
                point = 1
            else:
                point = 0
            p += int(credit) * point
        try:
            gpa = (p / total_credit_in_semester)
            return round(gpa, 2)
        except ZeroDivisionError:
            return 0
    
    def calculate_cgpa(self):
        current_semester = Semester.objects.get(is_current_semester=True)
        previousResult = Result.objects.filter(student__id=self.student.id, level__lt=self.student.level)
        previousCGPA = 0
        for i in previousResult:
            if i.cgpa is not None:
                previousCGPA += i.cgpa
        cgpa = 0
        if str(current_semester) == SECOND:
            first_sem_gpa = 0.0
            sec_sem_gpa = 0.0
            try:
                first_sem_result = Result.objects.get(student=self.student.id, semester=FIRST, level=self.student.level)
                first_sem_gpa += first_sem_result.gpa
            except:
                first_sem_gpa = 0

            try:
                sec_sem_result = Result.objects.get(student=self.student.id, semester=SECOND, level=self.student.level)
                sec_sem_gpa += sec_sem_result.gpa
            except:
                sec_sem_gpa = 0

            taken_courses = TakenCourse.objects.filter(student=self.student, student__level=self.student.level)
            TCC = 0
            TCP = 0
            for i in taken_courses:
                TCP += float(i.point)
            for i in taken_courses:
                TCC += int(i.course.credit)
            # cgpa = (first_sem_gpa + sec_sem_gpa) / 2

            print("TCP = ", TCP)
            print("TCC = ", TCC)
            print("first_sem_gpa = ", first_sem_gpa)
            print("sec_sem_gpa = ", sec_sem_gpa)
            print("cgpa = ", round(TCP / TCC, 2))

            try:
                cgpa = TCP / TCC
                return round(cgpa, 2)
            except ZeroDivisionError:
                return 0

            # return round(cgpa, 2)


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    gpa = models.FloatField(null=True)
    cgpa = models.FloatField(null=True)
    semester = models.CharField(max_length=100, choices=SEMESTER)
    session = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
