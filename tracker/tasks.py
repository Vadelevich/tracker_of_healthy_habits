from datetime import timedelta, datetime
from celery import shared_task
from tracker.models import Habit
from users.telegram import send_message


@shared_task
def check_time():
    time = datetime.now().time()
    time_start_task = datetime.now() - timedelta(minutes=1)
    data_habit = Habit.objects.filter(time__gte=time_start_task)
    for item in data_habit.filter(time__lte=time):
        text = f'я буду {item.action} в {item.time} в {item.place}'
        send_message(text)







