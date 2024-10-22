# import custom django user model
from django.contrib.auth.hashers import make_password

# work with json file so that  ur front-end can work with it
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserModel


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = UserModel
        fields = (
            "username",
            "password",
            "confirm_password",
            "email",
            "first_name",
            "last_name",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    # called when user is saved automatically
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data["password"] = make_password(validated_data["password"])
        user = UserModel(**validated_data)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
