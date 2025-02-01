from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from books.models import Book
from books.serializers import BookSerializer
from .recommendations import get_recommendations
from .serializers import FavoriteBookSerializer

# Create your views here.


@extend_schema(
    tags=["Favorite"],
)
class FavoriteBookView(generics.GenericAPIView):
    serializer_class = FavoriteBookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        favorite_books = user.favorite_books.all()
        serializer = BookSerializer(favorite_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        book_id = request.data.get("book_id")

        if user.favorite_books.count() > 20:
            return Response(
                {"message", "You can only have 20 favorite books"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            book = Book.objects.get(id=book_id)
            user.favorite_books.add(book)
            user.save()
            recommendations = get_recommendations(user.favorite_books.all())
            return Response(
                {
                    "message": "Book added to favorites",
                    "recommendations": BookSerializer(recommendations, many=True).data,
                },
                status=status.HTTP_200_OK,
            )
        except Book.DoesNotExist:
            return Response(
                {"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request):
        user = request.user
        book_id = request.data.get("book_id")
        try:
            book = Book.objects.get(id=book_id)
            user.favorite_books.remove(book)
            user.save()
            recommendations = get_recommendations(user.favorite_books.all())
            return Response(
                {
                    "message": "Book removed from favorites",
                    "recommendations": BookSerializer(recommendations, many=True).data,
                },
                status=status.HTTP_200_OK,
            )
        except Book.DoesNotExist:
            return Response(
                {"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )


favorite_book = FavoriteBookView.as_view()
