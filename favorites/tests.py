from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import CustomUser
from books.models import Book
from authors.models import Author


class FavoritesAPITest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test", email="test@mail.com", password="test"
        )
        self.author = Author.objects.create(name='author')
        self.book = Book.objects.create(title="test", isbn="123456789", author=self.author)
        self.url = reverse("favorite_books")
        response = self.client.post(
            reverse("login"), {"email": "test@mail.com", "password": "test"}
        )
        self.header = {"Authorization": f"Bearer {response.json()['access']}"}

    def test_favorite_book(self):
        data = {"book_id": self.book.id}
        response = self.client.post(self.url, data, headers=self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_favorite_books(self):
        response = self.client.get(self.url, headers=self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_favorite_book(self):
        self.client.force_authenticate(user=self.user)
        data = {"book_id": self.book.id}
        response = self.client.delete(self.url, data, headers=self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
