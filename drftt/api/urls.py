"""drftt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.urls import path, include
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'level', views.GameLevelViewSet)
# router.register(r'team', views.TeamViewSet)
# router.register(r'gameplay', views.GamePlayViewSet)
# router.register(r'game', views.GameViewSet)

app_name = 'api'

urlpatterns = [
    path('game/', views.GameList.as_view()),
    path('game/<int:pk>', views.GameDetail.as_view()),
    path('team/', views.TeamList.as_view()),
    path('team/<int:pk>', views.TeamDetail.as_view()),
    path('answer/', views.AnswersList.as_view()),
    path('answer/<int:pk>', views.AnswerDetail.as_view()),
    # path('promt/', views.PromtList.as_view()),
    # path('promt/<int:pk>/', views.PromtDetail.as_view()),
    path('gameplay/', views.GamePlayList.as_view()),
    path('gameplay/<int:pk>/', views.GamePlayDetail.as_view()),
    path('level/', views.GameLevelList.as_view()),
    path('level/<int:pk>/', views.GameLevelDetail.as_view()),
    path('level/<int:pk>/promt<int:num>', views.GetPromt.as_view()),
    path('level/<int:pk>/answer?<str:answer>', views.AnswerDetail.as_view()),
    # path('', include(router.urls)),

    ]