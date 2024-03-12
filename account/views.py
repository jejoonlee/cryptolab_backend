from django.shortcuts import render
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.response import Response


# Create your views here.
class UserView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            userResponse = {
                "Message": serializer.data["name"] + "님 성공적으로 회원가입을 했습니다",
                "email": serializer.data["email"],
            }

            return Response(userResponse, status=201)

        else:
            return Response(serializer.errors, status=400)