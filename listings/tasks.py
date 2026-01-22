from celery import shared_task
from django.core.mail import send_mail


@shared_task
def example_add(x, y):
	return x + y


@shared_task
def send_notification_email(subject, message, recipient):
    send_mail(
        subject,
        message,
        "noreply@yourapp.com",
        [recipient],
        fail_silently=False,
    )
    return f"Email sent to {recipient}"
