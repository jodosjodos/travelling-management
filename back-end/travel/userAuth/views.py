from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from .models import UserModel


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {"username": user.username, "message": "user registered successfully"},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# login fnc
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        # compare  hashed password and    raw  password
        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        # generate token
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "message": "Login successfully",
            },
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# protected route to get user info
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    # Get the authenticated user
    user = request.user

    # Check if the user exists (this should not be necessary if you're using IsAuthenticated)
    if user is None:
        return Response(
            {"detail": "User not found", "code": "user_not_found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Prepare user data to return
    user_data = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    return Response(
        {"user": user_data, "message": "User info retrieved successfully"},
        status=status.HTTP_200_OK,
    )
