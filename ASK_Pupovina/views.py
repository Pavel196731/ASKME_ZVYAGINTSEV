from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return render(request, 'ASK_Pupovina/base.html')

def stranica(request):
    return render(request, 'ASK_Pupovina/about.html')