from rest_framework.test import APITestCase
from django.urls import reverse

from app_course.models import Course, Lesson, Subscription
from users.models import User
from rest_framework import status


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com', is_staff=True, is_superuser=True)
        self.user.set_password('1234')
        self.user.save()

        response = self.client.post(
            '/users/token/',
            {'email': 'test@test.com', 'password': "1234"}
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.data = {
            'name': 'Test',
            'description': 'test description',
            'video': 'https://www.youtube.com/watch?v=g10qKRsi28U',
        }

    def test_create_lesson(self):
        response = self.client.post(
            reverse('app_course:lesson_create'),
            self.data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": response.json()['id'],
                "name": "Test",
                "description": "test description",
                "preview": None,
                "video": "https://www.youtube.com/watch?v=g10qKRsi28U",
                "course": None,
                "owner": self.user.pk
            }
        )

    def test_list_lesson(self):
        self.test_create_lesson()
        response = self.client.get(reverse('app_course:lessons'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['results'],
            [
                {
                    "id": response.json()['results'][0]['id'],
                    "name": "Test",
                    "description": "test description",
                    "preview": None,
                    "video": "https://www.youtube.com/watch?v=g10qKRsi28U",
                    "course": None,
                    "owner": self.user.pk
                }
            ]
        )

    def test_retrieve_lesson(self):
        self.test_create_lesson()
        pk = Lesson.objects.all().latest('pk').pk
        response = self.client.get(f'/lesson/{pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": pk,
                "name": "Test",
                "description": "test description",
                "preview": None,
                "video": "https://www.youtube.com/watch?v=g10qKRsi28U",
                "course": None,
                "owner": self.user.pk
            }
        )

    def test_update_lesson(self):
        self.test_create_lesson()
        pk = Lesson.objects.all().latest('pk').pk
        response = self.client.patch(f'/lesson/update/{pk}/', {'name': 'Test changed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": pk,
                "name": "Test changed",
                "description": "test description",
                "preview": None,
                "video": "https://www.youtube.com/watch?v=g10qKRsi28U",
                "course": None,
                "owner": self.user.pk
            }
        )

    def test_destroy_lesson(self):
        self.test_create_lesson()
        pk = Lesson.objects.all().latest('pk').pk
        response = self.client.delete(f'/lesson/delete/{pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com', is_staff=True, is_superuser=True)
        self.user.set_password('1234')
        self.user.save()

        response = self.client.post(
            '/users/token/',
            {'email': 'test@test.com', 'password': "1234"}
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(name='Test course', description='Test description')

        self.data = {
            'course': self.course.pk,
            'user': self.user.pk,
            'status': True
        }

    def test_create_subscription(self):
        response = self.client.post('/subscription/create', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": response.json()['id'],
                'course': self.course.pk,
                'user': self.user.pk,
                'status': True
            }
        )

    def test_destroy_subscription(self):
        self.test_create_subscription()
        pk = Subscription.objects.all().latest('pk').pk
        response = self.client.delete(f'/subscription/delete/{pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)