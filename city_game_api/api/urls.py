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
from . import views
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('game/<int:game>/level/', views.GameLevelList.as_view(), name='game'),
    path('game/<int:game>/level/<int:pk>/', views.GameLevelDetail.as_view(), name='level'),
    path('game/<int:game>/level/<int:pk>/promt/<int:num>/', views.GetPromt.as_view(), name='promt'),
    path('answer/', views.AnswerDetail.as_view(), name='answer'),
    path('stat/<int:game>/', views.game_summary),
]
