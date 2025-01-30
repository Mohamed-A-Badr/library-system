from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        email = attrs["email"]
        username = attrs["username"]

        if email and CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("This Email already exists")
        if username and CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("This Username already exists")

        return super().validate(attrs)

    def create(self, validated_data):
        try:
            user = CustomUser.objects.create_user(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return user
