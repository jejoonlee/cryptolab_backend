from .models import User

from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    name = serializers.CharField(required=True)

    password = serializers.CharField(required=True, validators=[validate_password])

    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "name", "password", "password2")

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"passwordInvalid": "비밀번호가 일치하지 않습니다"}
            )

        return data

    def create(self, validate_data):

        user = User.objects.create_user(
            email = validate_data["email"],
            name = validate_data["name"],
            password = validate_data["password"]
        )

        return user