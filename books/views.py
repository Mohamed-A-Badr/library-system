from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from .models import Book
from .serializers import BookSerializer


@extend_schema(
    tags=["Book"],
    summary="List Books or Create new one",
    description="Endpoint for list all books or create a new one",
)
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


@extend_schema(
    tags=["Book"],
    summary="Retrieve date for specific Book, update or delete one",
    description="Endpoint for retrieving the information of a specific Book, update, or delete one",
)
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "pk"


book_list = BookListView.as_view()
book_detail = BookDetailView.as_view()
