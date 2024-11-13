"""
URL configuration for ASKME_Zvyagintsev project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authorized/', views.main_authorized, name='main_authorized'),
    path('ask/', views.ask, name='ask'),
    path('setting/', views.setting, name='setting'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('answer/', views.answer, name='answer'),
    path('one_question/tag/<str:tag>/', views.tags, name='tags'),
    path('logout/', views.logout, name='logout'),
    path('one_question/<int:question_id>/', views.one_question, name='one_question'),
    path('admin/', admin.site.urls),


    path('Profile_list/', views.Profile_list, name='Profile_list'),
    path('Profile_list/Profile_detail/<int:pk>/', views.Profile_detail, name='question_detail'),
]
