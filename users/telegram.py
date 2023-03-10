import requests
from django.conf import settings
from rest_framework.response import Response

from tracker.models import Habit


def send_message(text):
    habit_data = Habit.objects.last()
    data_for_request = {
        "chat_id": "-1001895570450",
        "text": text
    }
    responce = requests.get(f'https://api.telegram.org/bot6027295301:AAENmIpfe9KP4YeoSrfLvvauhuHirKfewgI/sendMessage',
                            data_for_request)
    return Response(responce.json())
