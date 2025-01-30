from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, permissions
from django.db.models import Q


from .models import Book
from .serializers import BookSerializer


@extend_schema(
    tags=["Book"],
    summary="List Books or Create new one",
    description="Endpoint for list all books or create a new one",
    parameters=[
        OpenApiParameter(
            name="search",
            description="Search books by title or author name",
            required=False,
            type=str,
        ),
    ],
)
class BookListView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        self.queryset = Book.objects.all()
        search = self.request.query_params.get("search", None)
        if search:
            self.queryset = self.queryset.filter(
                Q(title__icontains=search) | Q(author__name__icontains=search)
            )
        return self.queryset


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
