from rest_framework.test import APITestCase
from rest_framework import status

from tracker.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User(email='12reqw@fsd.ru')
        self.user.set_password('123qwe456')
        self.user.save()

        response = self.client.post("/users/api/token/", {"email": "12reqw@fsd.ru", "password": "123qwe456"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data_for_responce = {
            "place": "Где нибудь",
            "time": "12:58",
            "action": "jhvhdsdcv",
            "time_to_complete": "00:02:00",
            "frequency": "1"

        }
        self.habit = Habit.objects.create(user=self.user, pleasant=True, **data_for_responce)

    def test_create_habit(self):
        data_for_responce = {
            "place": "Где нибудь",
            "time": "12:58",
            "action": "jhvhdsdcv",
            "pleasant": "True",
            "time_to_complete": "00:02:00",
            "frequency": "1"

        }
        responce = self.client.post('/tracker/create_habit/', data_for_responce)
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_update_habit(self):
        data_for_responce = {
            "place": "Где нибудь",
            "time": "12:58",
            "action": "jhvhdsdcv",
            "pleasant": "True",
            "time_to_complete": "00:02:00",
            "frequency": "1"

        }
        responce = self.client.put(f'/tracker/update_habit/{self.habit.pk}/', data_for_responce)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_detail_habit(self):
        responce = self.client.get(f'/tracker/retrieve_habit/{self.habit.pk}/')
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_list_habit(self):
        responce = self.client.get('/tracker/list_habit/')
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_list_all_habit(self):
        responce = self.client.get('/tracker/all_list_habit/')
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_delete_habit(self):
        responce = self.client.delete(f'/tracker/destroy_habit/{self.habit.pk}/')
        self.assertEqual(responce.status_code, status.HTTP_204_NO_CONTENT)


class HabitValidateTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User(email='12reqw@fsd.ru')
        self.user.set_password('123qwe456')
        self.user.save()

        response = self.client.post("/users/api/token/", {"email": "12reqw@fsd.ru", "password": "123qwe456"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data_for_responce = {
            "place": "Где нибудь",
            "time": "12:58",
            "action": "jhvhdsdcv",
            "time_to_complete": "00:02:00",
            "frequency": "1"

        }
        self.habit = Habit.objects.create(user=self.user, pleasant=True, **data_for_responce)
        self.habit2 = Habit.objects.create(user=self.user, pleasant=False, **data_for_responce)

    def test_create_validate_time(self):
        data_for_responce = {
            "place": "Где нибудь",
            "time": "12:58",
            "action": "jhvhdsdcv",
            "pleasant": "True",
            "time_to_complete": "00:02:01",
            "frequency": "1"

        }
        responce = self.client.post('/tracker/create_habit/', data_for_responce)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = {
            "non_field_errors": [
                "привычка не должна расходовать на выполнение больше 2х минут"
            ]
        }
        self.assertEqual(responce.json(), expected_data)

    def test_create_validate_two_pleasant(self):
        data_for_responce = {
            "place": "Где нибудь",
            "time": "12:58",
            "action": "jhvhdsdcv",
            "pleasant": "True",
            "time_to_complete": "00:02:00",
            "connection": self.habit.pk

        }
        responce = self.client.post('/tracker/create_habit/', data_for_responce)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = {
            "non_field_errors": [
                "Нельзя связать две приятные привычки!",
                "у приятной привычки не может быть вознаграждения или связанной привычки"
            ]
        }
        self.assertEqual(responce.json(), expected_data)

    def test_validate_award_connection_null(self):
        data_for_responce = {
            "place": "Где нибудь",
            "time": "12:58",
            "action": "jhvhdsdcv",
            "pleasant": "False",
            "time_to_complete": "00:02:00"

        }
        responce = self.client.post('/tracker/create_habit/', data_for_responce)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = {
            "non_field_errors": [
                " Нельзя, чтобы связанная привычка и вознаграждение были одновременно пустые"
            ]
        }
        self.assertEqual(responce.json(), expected_data)
        data_for_responce = {
            "place": "Где нибудь",
            "time": "12:58",
            "action": "jhvhdsdcv",
            "pleasant": "True",
            "time_to_complete": "00:02:00"

        }
        responce = self.client.post('/tracker/create_habit/', data_for_responce)
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)

    def test_validate_award(self):
        data_for_responce = {
            "place": "Где нибудь",
            "time": "12:58",
            "action": "jhvhdsdcv",
            "pleasant": "True",
            "time_to_complete": "00:02:00",
            "award": "bsbxxb"

        }
        responce = self.client.post('/tracker/create_habit/', data_for_responce)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = {
            "non_field_errors": [
                "у приятной привычки не может быть вознаграждения или связанной привычки"
            ]
        }
        self.assertEqual(responce.json(), expected_data)

    def test_validate_pleasant_FalseOrTrue(self):
        data_for_responce = {
            "place": "Где нибудь",
            "time": "12:58",
            "action": "jhvhdsdcv",
            "pleasant": "True",
            "time_to_complete": "00:02:00",
            "connection": self.habit2.pk

        }
        responce = self.client.post('/tracker/create_habit/', data_for_responce)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = {
            "non_field_errors": [
                "в связанные привычки могут попадать только привычки с признаком приятной привычки",
                "у приятной привычки не может быть вознаграждения или связанной привычки"
            ]
        }
        self.assertEqual(responce.json(), expected_data)

    def test_validate_and_award_and_connection(self):
        data_for_responce = {
            "place": "Где нибудь",
            "time": "12:58",
            "action": "jhvhdsdcv",
            "pleasant": "True",
            "time_to_complete": "00:02:00",
            "award": "shvahvsa"

        }
        responce = self.client.post('/tracker/create_habit/', data_for_responce)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = {
            "non_field_errors": [
                "у приятной привычки не может быть вознаграждения или связанной привычки"
            ]
        }
        self.assertEqual(responce.json(), expected_data)

    def test_frequency(self):
        data_for_responce = {
            "place": "Где нибудь",
            "time": "12:58",
            "action": "jhvhdsdcv",
            "pleasant": "True",
            "time_to_complete": "00:02:00",
            "frequency": 8

        }
        responce = self.client.post('/tracker/create_habit/', data_for_responce)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = {
            "non_field_errors": [
                "периодичность не может быть более 7 дней, то есть привычку нельзя выполнять больше, чем раз в неделю"
            ]
        }
        self.assertEqual(responce.json(), expected_data)
