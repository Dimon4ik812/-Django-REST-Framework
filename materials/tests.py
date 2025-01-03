from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from materials.models import Course, Lesson, Subscription
from users.models import CustomsUser

User = get_user_model()


class CourseTestCase(APITestCase):
    """Тестовый класс для тестирования куса"""

    def setUp(self):
        self.user = CustomsUser.objects.create(email="testuser@example.com", is_active=True)
        self.user.set_password("testpassword")
        self.user.save()

        self.access_token = AccessToken.for_user(self.user)

    def test_create_course(self):
        """Тестирование создания курса"""
        data = {"title": "test", "description": "test", "owner": self.user.id}
        response = self.client.post("/course/", data=data, HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Course.objects.filter(title="test").exists())
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().title, "test")


class LessonPlatformTestCase(APITestCase):
    """Тестовый класс для тестирования уроков, а так же подписки на урок"""

    def setUp(self):
        self.user = CustomsUser.objects.create(email="testuser@example.com", is_active=True)
        self.user.set_password("testpassword")
        self.user.save()

        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {
            "title": "Test Lesson",
            "description": "Description",
            "course": self.course.id,
            "video_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "owner": self.user.id,
        }
        response = self.client.post("/lesson/create/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #
    def test_list_lessons(self):
        """Тестирование получения списка уроков"""
        # Создание 4 уроков
        for i in range(1, 5):
            Lesson.objects.create(
                title=f"Test Lesson {i}",
                description=f"Description {i}",
                course=self.course,
                video_link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                owner=self.user,
            )

        response = self.client.get("/lesson/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_lesson(self):
        """Тестирование получения конкретного урока"""
        lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Description",
            course=self.course,
            video_link="http://www.youtube.com/1",
            owner=self.user,
        )

        response = self.client.get(f"/lesson/{lesson.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Lesson")

    def test_update_lesson(self):
        lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Description",
            course=self.course,
            video_link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            owner=self.user,
        )

        data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "course": self.course.id,
            "video_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        }
        response = self.client.put(f"/lesson/update/{lesson.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Description",
            course=self.course,
            video_link="http://www.youtube.com/1",
            owner=self.user,
        )

        response = self.client.delete(f"/lesson/delete/{lesson.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=lesson.id).exists())

    def test_subscription(self):
        """Тестирование подписки на обновления курса"""
        response = self.client.post("/subscription/", {"course_id": self.course.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
