from .models import Article
from .serializers import ArticleSerializer
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404

# Create your views here.
class ArticleList(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)

        response = []

        for data in serializer.data:
            response.append({
                "글 번호" : data["id"],
                "글 제목" :  data["title"],
                "등록 시간" : data["createdAt"],
                "작성자" : "user",
            })

        return Response(response, status = status.HTTP_200_OK)


    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message" : "글이 작성되었습니다",
                "id" : serializer.data["id"],
                "title" : serializer.data["title"]
            }

            return Response(response, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetail(APIView):
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        article = self.get_object(pk)
        
        serializer = ArticleSerializer(article)

        response = {
            "글 번호" : serializer.data["id"],
            "글 제목" :  serializer.data["title"],
            "글 내용" : serializer.data["content"],
            "등록 시간" : serializer.data["createdAt"],
            "작성자" : "user",
        }

        return Response(response, status = status.HTTP_200_OK)
    
    def delete(self, request, pk, format=None):
        article = self.get_object(pk)
        article.delete()

        response = {
            "message" : "글이 삭제 되었습니다"
        }

        return Response(response, status=status.HTTP_200_OK)      