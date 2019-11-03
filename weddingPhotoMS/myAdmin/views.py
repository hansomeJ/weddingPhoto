from io import BytesIO

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse

from cameraman.models import Cameraman
from customer.models import Customer
from myAdmin.models import Admin
from cameraman.models import Cameraman
from customer.models import Customer

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods, require_safe

from django.http import JsonResponse, HttpResponse

from weddingPhotoMS.utils import create_code, pwd_by_hashlib, pwd_by_hmac


# Create your views here.

def code(request):
    """验证码的视图函数"""
    # 通过工具类获取图片对象和图上的值
    img, msg = create_code()
    # 获取一个字节IO
    file = BytesIO()
    img.save(file, "PNG")
    # 将验证码的值存储到session
    request.session["code"] = msg
    image = file.getvalue()
    # MIME 文件类型
    return HttpResponse(image)


@require_POST
@csrf_exempt
def register(request):
    name = request.POST.get('name').strip()
    pwd = request.POST.get('pwd').strip()
    pwd2 = request.POST.get('pwd2').strip()
    type = request.POST.get('type').strip()
    code = request.POST.get('code').strip()
    print(name, pwd, pwd2, type, code)
    code_real = request.session['code']
    if code_real.lower() != code:
        return JsonResponse({'code_error': 1})
    pwd_new = pwd_by_hmac(pwd)
    if type == '管理员':
        try:
            Admin.objects.get(admin_Name=name)
            # 用户名已存在
            return JsonResponse({'name': 1})
        except Exception as e:
            try:
                user = Admin(admin_Name=name, admin_pwd=pwd_new)
                user.save()
                result = {'Success': True}
                return JsonResponse(result)
            except Exception as e:
                print(e)
                return JsonResponse({'Failed': True})
    elif type == '摄影师':
        try:
            Cameraman.object.get(ca_name=name)
            return JsonResponse({'name': 1})
        except Exception as e:
            try:
                user = Cameraman(ca_name=name, ca_pwd=pwd_new)
                user.save()
                result = {'Success': True}
                return JsonResponse(result)
            except Exception as e:
                print(e)
                return JsonResponse({'Failed': True})
    else:
        try:
            Customer.objects.get(cs_name=name)
            return JsonResponse({'name': 1})
        except Exception as e:
            print(e)
            try:
                user = Customer(cs_name=name, cs_pwd=pwd_new)
                user.save()
                result = {'Success': True}
                return JsonResponse(result)
            except Exception as e:
                print(e)
                return JsonResponse({'Failed': True})


# 登录函数
@require_POST
@csrf_exempt
def login(request):
    name = request.POST.get('name').strip()
    pwd = request.POST.get('pwd').strip()
    type = request.POST.get('type').strip()
    code = request.POST.get('code').strip()
    code_real = request.session['code']
    if code_real.lower() != code:
        return JsonResponse({'code_error': 1})
    pwd_new = pwd_by_hmac(pwd)
    if type == '管理员':
        try:
            user = Admin.objects.get(admin_Name=name)
            if user.admin_pwd != pwd_new:
                # 密码错误
                return JsonResponse({'pwd_error': 1})
            else:
                # 用户名密码匹配，重定向到管理员首页面
                # return redirect(reverse('Admin:index'))
                result = {'Success': True}
                return JsonResponse(result)
        except Exception as e:
            # 该用户不存在
            print(e)
            return JsonResponse({'Failed': True})
    elif type == '摄影师':
        try:
            user = Cameraman.objects.get(ca_name=name)
            if user.ca_pwd != pwd_new:
                # 密码错误
                return JsonResponse({'pwd_error': 1})
            else:
                # 用户名密码匹配，重定向到管理员首页面
                # return redirect(reverse('Admin:index'))
                result = {'Success': True}
                return JsonResponse(result)
        except Exception as e:
            # 该用户不存在
            print(e)
            return JsonResponse({'Failed': True})
    else:
        try:
            user = Customer.objects.get(cs_name=name)
            if user.cs_pwd != pwd_new:
                # 密码错误
                return JsonResponse({'pwd_error': 1})
            else:
                # 用户名密码匹配，重定向到管理员首页面
                # return redirect(reverse('Admin:index'))
                result = {'Success': True}
                return JsonResponse(result)
        except Exception as e:
            # 该用户不存在
            print(e)
            return JsonResponse({'Failed': True})


# 管理员主界面函数
def index(request):
    if request.method == 'GET':
        return render(request, 'admin/index.html')
