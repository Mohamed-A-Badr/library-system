from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .models import CustomUser


# Create your tests here.
class TestCustomUserModel(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "test123",
        }

    def test_create_user(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(**self.user_data)
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class TestAccounts(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="testuser1",
            email="test1@example.com",
            password="test123",
        )

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.refresh_url = reverse("refresh")

    def test_register(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "test123",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        data = {
            "email": "test1@example.com",
            "password": "test123",
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh(self):
        response = self.client.post(
            self.login_url, {"email": "test1@example.com", "password": "test123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.json()["refresh"]
        data = {
            "refresh": refresh_token,
        }
        response = self.client.post(self.refresh_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
