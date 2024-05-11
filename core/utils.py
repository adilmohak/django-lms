from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_email(user, subject, msg):
    send_mail(
        subject,
        msg,
        settings.EMAIL_FROM_ADDRESS,
        [user.email],
        fail_silently=False,
    )


def send_html_email(subject, recipient_list, template, context):
    """A function responsible for sending HTML email"""
    # Render the HTML template
    html_message = render_to_string(template, context)

    # Generate plain text version of the email (optional)
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_FROM_ADDRESS,
        recipient_list,
        html_message=html_message,
    )
