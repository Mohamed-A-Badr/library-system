from rest_framework import generics

from .models import CustomUser
from .serializers import RegisterSerializer
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@extend_schema(
    tags=["Authentication"],
    summary="Registration for new users",
    description="Register new user and create it to save in the database",
)
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


@extend_schema(
    tags=["Authentication"],
    summary="Login to user account",
    description="Endpoint for login to user account",
)
class LoginView(TokenObtainPairView):
    pass


@extend_schema(
    tags=["Authentication"],
    summary="Refresh token",
    description="Endpoint for refreshing access token after expired",
)
class RefreshView(TokenRefreshView):
    pass


register = RegisterView.as_view()
login = LoginView.as_view()
refresh = RefreshView.as_view()
