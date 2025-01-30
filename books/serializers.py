from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = (
            "author_name",
            "author",
            "title",
            "description",
            "published_date",
            "language",
            "isbn",
            "publisher",
            "page_count",
            "categories",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {"author": {"write_only": True}}

    def get_author_name(self, obj):
        return obj.author.name

    def validate(self, attrs):
        isbn = attrs["isbn"]
        page_count = attrs["page_count"]
        if not isbn or not isbn.isdigit():
            raise serializers.ValidationError(
                "ISBN shouldn't be empty or contain any characters"
            )
        if not page_count or page_count < 0:
            raise serializers.ValidationError(
                "Number of pages shouldn't be empty or negative number"
            )
        return super().validate(attrs)
