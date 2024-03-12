from .models import User

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login

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
    

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def validate(self, data):

        user = authenticate(email = data.get("email"), password=data.get("password"))

        if user:
            if not user.is_active:
                raise serializers.ValidationError(
                    {"userInactive": "계정이 비활성화 되어 있습니다"}
                )
        
        else:
            raise serializers.ValidationError(
                {"InvalidInput" : "이메일 또는 비밀번호를 잘 못 입력했습니다"}
            )

        return data
    
    def login_now(self, request):
        user = authenticate(email = request.data['email'], password=request.data['password'])
        if user:
            login(request, user)
        return user