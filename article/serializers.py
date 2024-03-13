from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'

    user = serializers.ReadOnlyField(source="user.email")

    # 사용자 정보가 자동으로 채워지도록 perform_create 메소드를 오버라이드합니다.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)