
from django.urls import path
from . import views

urlpatterns = [
    path('ASK_Pupovina/', views.index, name='ASK_Pupovina'),
    path('ASK_Pupovina/stranica/', views.stranica, name='stranica')
]