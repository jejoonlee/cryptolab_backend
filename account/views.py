from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response

# Create your views here.
class UserView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            userResponse = {
                "Message": serializer.data["name"]
                + "님 성공적으로 회원가입을 했습니다",
                "email": serializer.data["email"],
            }

            return Response(userResponse, status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(generics.CreateAPIView):

    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.login_now(request)
            if user:
                return Response({"message": "로그인 성공"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "유효하지 않은 자격 증명"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        