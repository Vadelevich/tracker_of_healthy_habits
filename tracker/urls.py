from django.urls import path

from tracker.views import HabitCreateAPIView, HabitUpdateAPIView, HabitRetrieveAPIView, HabitDestroyAPIView, \
    HabitAllPublicListAPIView, HabitListAPIView

urlpatterns = [
    path('create_habit/',HabitCreateAPIView.as_view()),
    path('list_habit/',HabitListAPIView.as_view()),
    path('update_habit/<int:pk>/',HabitUpdateAPIView.as_view()),
    path('retrieve_habit/<int:pk>/',HabitRetrieveAPIView.as_view()),
    path('destroy_habit/<int:pk>/',HabitDestroyAPIView.as_view()),
    path('all_list_habit/',HabitAllPublicListAPIView.as_view()),
]