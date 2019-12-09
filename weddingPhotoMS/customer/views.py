import os
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

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods, require_safe

from django.http import JsonResponse, HttpResponse

from django.db.models import Q
from weddingPhotoMS.utils import create_code, pwd_by_hashlib, pwd_by_hmac


# Create your views here.

def index(request):
    return render(request, 'customer/index.html')


def addOrder(request):
    if request.method == 'GET':
        allbv = bv.objects.all()
        allbvs = bvs.objects.all()
        space = Space.objects.all()
        cameraman = Cameraman.objects.all()
        return render(request, 'customer/makeOrder.html',
                      {'allBv': allbv, 'allBvs': allbvs, 'space': space, 'cameraman': cameraman})
    else:
        return render(request, 'customer/index.html')