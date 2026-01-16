
from celery import shared_task

@shared_task
def example_add(x, y):
	return x + y

