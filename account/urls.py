from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    # 회원가입
    path("register", views.UserView.as_view())
    # 로그인
    # path('login', views.login, name='login')
    # 로그아웃
    # path('logout', views.logout, name='logout')
]
