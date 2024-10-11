
from django.urls import path
from . import views

urlpatterns = [
    path('ASK_Pupovina/', views.members, name='ASK_Pupovina'),
]