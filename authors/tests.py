from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import CustomUser

from .models import Author


# Create your tests here.
class AuthorModelTest(TestCase):
    def test_create_author(self):
        author = Author.objects.create(
            name="Lorem ipsum",
            bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Erat enim Polemonis.",
        )
        self.assertEqual(author.name, "Lorem ipsum")
        self.assertEqual(
            author.bio,
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Erat enim Polemonis.",
        )


class AuthorViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="testuser", email="test1@example.com", password="test123"
        )

    def setUp(self):
        response = self.client.post(
            reverse("login"), {"email": "test1@example.com", "password": "test123"}
        )
        self.access_token = response.json()["access"]

    def test_list_authors(self):
        authors = [
            Author.objects.create(
                name="Lorem ipsum",
                bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Erat enim Polemonis.",
            ),
            Author.objects.create(name="test author", bio="test author bio"),
        ]
        url = reverse("author_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], authors[0].name)
        self.assertEqual(response.data[0]["bio"], authors[0].bio)
        self.assertEqual(response.data[1]["name"], authors[1].name)
        self.assertEqual(response.data[1]["bio"], authors[1].bio)

    def test_detail_author(self):
        author = Author.objects.create(
            name="Lorem ipsum",
            bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Erat enim Polemonis.",
        )
        url = reverse("author_detail", kwargs={"pk": author.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], author.name)
        self.assertEqual(response.data["bio"], author.bio)

    def test_create_author(self):
        url = reverse("author_list")
        data = {
            "name": "test author",
            "bio": "test author bio",
        }
        header = {
            "Authorization": f"Bearer {self.access_token}",
        }
        response = self.client.post(url, data, headers=header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["bio"], data["bio"])

    def test_update_author(self):
        author = Author.objects.create(
            name="Lorem ipsum",
            bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Erat enim Polemonis.",
        )
        url = reverse("author_detail", kwargs={"pk": author.pk})
        data = {
            "name": "test author",
            "bio": "test author bio",
        }
        header = {
            "Authorization": f"Bearer {self.access_token}",
        }
        response = self.client.put(url, data, headers=header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["bio"], data["bio"])

    def test_delete_author(self):
        author = Author.objects.create(
            name="Lorem ipsum",
            bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Erat enim Polemonis.",
        )
        header = {
            "Authorization": f"Bearer {self.access_token}",
        }
        url = reverse("author_detail", kwargs={"pk": author.pk})
        response = self.client.delete(url, headers=header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
