from django.shortcuts import render
from cameraman.models import Cameraman
from customer.models import Customer
from myAdmin.models import Admin

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods, require_safe

from django.http import JsonResponse,HttpResponse


# Create your views here.
@require_POST
@csrf_exempt
def register(request):
    name = request.POST.get('name').strip()
    pwd = request.POST.get('pwd').strip()
    pwd2 = request.POST.get('pwd2').strip()
    type = request.POST.get('type').strip()
    code = request.POST.get('code').strip()
    print(name, pwd, pwd2, type, code)
    result = {'Success': True}
    return JsonResponse({'Success': True})
    # return render(request, 'base.html')
