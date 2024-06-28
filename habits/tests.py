from datetime import timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """ Тестирование модели Habit """

    def setUp(self):
        """ Метод для предоставления тестового объекта """

        self.client = APIClient()
        # Создание Пользователя
        self.user = User.objects.create(
            email="test@sky.pro",
            password="test",
        )
        # Аутентификация клиента с помощью метода force_authenticate
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            owner=self.user,
            place="На улице",
            time="12:00:00",
            action="Выполнить 50 приседаний",
            pleasant_habit=False,
            periodicity=1,
            reward="Получишь шоколадное мороженное",
            time_required=timedelta(seconds=90),
            public_visibility=True,
        )

    def test_habit_create(self):
        """ Тест на создание новой привычки """

        url = reverse("habits:habit_create")
        data = {
            "owner": self.user.pk,
            "place": "test_place",
            "time": "12:00:00",
            "action": "test_action",
            "pleasant_habit": False,
            "periodicity": 1,
            "reward": "test_reward",
            "time_required": '00:01:30',
            "public_visibility": True,
        }
        # POST запрос
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_delete(self):
        """ Тест на удаление привычки """
        url = reverse("habits:habit_delete", args=(self.habit.pk,))
        # DELETE запрос
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Habit.objects.all().count(),
            0,
        )

    def test_habit_retrieve(self):
        """ Тест на получение данных привычки """

        url = reverse("habits:habit_detail", args=(self.habit.pk,))
        # GET запрос
        response = self.client.get(url)
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get("reward"),
            self.habit.reward,
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.habit.id,
                "owner": self.user.pk,
                "place": "На улице",
                "time": '12:00:00',
                "action": "Выполнить 50 приседаний",
                "pleasant_habit": False,
                "periodicity": 1,
                "reward": "Получишь шоколадное мороженное",
                "time_required": '00:01:30',
                "public_visibility": True,
                "linked_habit": None,
            },
        )

    def test_habit_update(self):
        """ Тест на редактирование данных привычки """

        url = reverse("habits:habit_change", args=(self.habit.pk,))
        # Данные для внесения изменений:
        data = {
            "reward": "Test_reward",
        }
        # PATCH запрос
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get("reward"),
            "Test_reward",
        )

    def test_habit_list(self):
        """ Тест на проверку работы пагинации """
        url = reverse("habits:habit_list")
        # GET запрос
        response = self.client.get(url)
        data = response.json()
        print(data)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.id,
                    "owner": self.user.id,
                    "place": "На улице",
                    "time": "12:00:00",
                    "action": "Выполнить 50 приседаний",
                    "pleasant_habit": False,
                    "periodicity": 1,
                    "reward": "Получишь шоколадное мороженное",
                    "time_required": '00:01:30',
                    "public_visibility": True,
                    "linked_habit": None,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK),
        self.assertEqual(data, result)

    def test_public_habit_list(self):
        """ Тест на проверку работы пагинации и вывода всех публичных привычек на страницу """

        url = reverse("habits:habit_public_list")
        # GET запрос
        response = self.client.get(url)
        # data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_execution_duration_habit(self):
        """ Тестирование создания привычки со временем исполнения более 2 минут """

        url = reverse("habits:habit_create")
        data = {
            "place": "test_place",
            "time": "12:00:00",
            "action": "test_action",
            "pleasant_habit": False,
            "linked_habit": 4,
            "time_required": 150,
            "public_visibility": True,
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_periodicity_habit(self):
        """ Тестирование создания привычки с периодичностью больше 7 дней """

        url = reverse("habits:habit_create")
        data = {
            "place": "test_place2",
            "time": "13:00:00",
            "action": "test_action2",
            "pleasant_habit": False,
            "linked_habit": 4,
            "time_required": 110,
            "periodicity": 8,
            "public_visibility": True,
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
