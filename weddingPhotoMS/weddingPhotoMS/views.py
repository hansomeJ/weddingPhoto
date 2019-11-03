from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from weddingPhotoMS.utils import create_code

def index(request):
    if request.method == 'GET':
        return render(request, 'base.html')
