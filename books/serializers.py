from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

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
