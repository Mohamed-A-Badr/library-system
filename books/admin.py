from django.contrib import admin
from .models import Book

# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "language",
        "isbn",
        "page_count",
        "publisher",
        "published_date",
    )
    list_filter = (
        "categories",
        "publisher",
        "created_at",
        "language",
    )
    search_fields = (
        "title",
        "publisher",
        "isbn",
    )
