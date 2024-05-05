import time
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


def send_email(user, subject, msg):
    send_mail(
        subject,
        msg,
        settings.EMAIL_FROM_ADDRESS,
        [user.email],
        fail_silently=False,
    )


@shared_task
def send_new_student_email(user_pk, password):
    user = get_user_model().objects.get(pk=user_pk)
    subject = "Your Dj LMS account credentials"
    msg = f"Dear Student {user.first_name},\n\nHere are the login credentials for your DJ LMS account.\n\nYour ID: {user.username}\nYour password: {password}\n\nBe sure to change your password for security."
    send_email(user, subject, msg)


@shared_task
def send_new_lecturer_email(user_pk, password):
    user = get_user_model().objects.get(pk=user_pk)
    subject = "Your Dj LMS account credentials"
    msg = f"Dear Lecturer {user.first_name},\n\nHere are the login credentials for your DJ LMS account.\n\nYour ID: {user.username}\nYour password: {password}\n\nBe sure to change your password for security."
    send_email(user, subject, msg)
