import os
import datetime
from io import BytesIO

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse

from myAdmin.models import Admin
from myAdmin.models import Bridal_Veil as bv
from myAdmin.models import Bridal_Veils as bvs
from myAdmin.models import Space
from myAdmin.models import Notice
from cameraman.models import Cameraman
from customer.models import Customer
from customer.models import Order

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods, require_safe

from django.http import JsonResponse, HttpResponse

from django.db.models import Q
from weddingPhotoMS.utils import create_code, pwd_by_hashlib, pwd_by_hmac


# Create your views here.
def index(request):
    return render(request, 'cameraman/index.html')


def showMsg(request):
    name = request.session['login_cameraman']['name']
    print(name)
    user = Cameraman.objects.get(ca_name=name)
    return render(request, 'cameraman/showMsg.html', {"user": user})
