from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import CustomUser
from authors.models import Author

from .models import Book


# Create your tests here.
class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="test")
        self.book = Book.objects.create(
            title="test", isbn="123456789", author=self.author
        )

    def test_book_model(self):
        self.assertEqual(self.book.title, "test")
        self.assertEqual(self.book.author, self.author)


class BooksAPITest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="test")
        self.book = Book.objects.create(
            title="test", isbn="123456789", author=self.author
        )
        self.user = CustomUser.objects.create_user(
            username="test", email="test@mail.com", password="test"
        )
        response = self.client.post(
            reverse("login"), {"email": "test@mail.com", "password": "test"}
        )
        self.access_token = response.json()["access"]

    def test_get_books_list(self):
        url = reverse("books_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_book_detail(self):
        url = reverse("book_detail", kwargs={"pk": self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_create_book(self):
        url = reverse("books_list")
        data = {
            "title": "test2",
            "isbn": "123456789",
            "page_count": 1000,
            "author": self.author.pk,
        }
        header = {
            "Authorization": f"Bearer {self.access_token}",
        }
        response = self.client.post(url, data, headers=header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        url = reverse("book_detail", kwargs={"pk": self.book.pk})
        data = {
            "title": "test3",
            "isbn": "123456789",
            "page_count": 100,
            "author": self.author.pk,
        }
        header = {
            "Authorization": f"Bearer {self.access_token}",
        }
        response = self.client.patch(url, data, headers=header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        url = reverse("book_detail", kwargs={"pk": self.book.pk})
        header = {
            "Authorization": f"Bearer {self.access_token}",
        }
        response = self.client.delete(url, headers=header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
