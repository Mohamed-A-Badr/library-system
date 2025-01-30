from django.urls import path

from . import views

urlpatterns = [
    path("favorite/", views.favorite_book, name="favorite_books"),
]
