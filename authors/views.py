from rest_framework import generics
from .serializers import AuthorSerializer
from .models import Author
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Author"],
    summary="List Authors or Create new one",
    description="Endpoint for list all authors or create a new one",
)
class AuthorListView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


@extend_schema(
    tags=["Author"],
    summary="Retrieve date for specific Author, update or delete one",
    description="Endpoint for retrieving the information of a specific author, update, or delete one",
)
class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = "pk"


author_list = AuthorListView.as_view()
author_detail = AuthorDetailView.as_view()
