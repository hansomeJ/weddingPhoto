import os
from io import BytesIO

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse

from cameraman.models import Cameraman
from customer.models import Customer
from myAdmin.models import Admin
from myAdmin.models import Bridal_Veil as bv
from myAdmin.models import Bridal_Veils as bvs
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
                # 用户名与密码匹配，登录成功
                result = {'Success': True}
                # 把管理员信息存入缓存
                request.session['login_admin'] = {'name': name}
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
                # 用户名与密码匹配，登录成功
                request.session['login_cameraman'] = {'name': name}
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
                # 用户名与密码匹配，登录成功
                request.session['login_user'] = {'name': name}
                result = {'Success': True}
                return JsonResponse(result)
        except Exception as e:
            # 该用户不存在
            print(e)
            return JsonResponse({'Failed': True})


# 管理员主界面函数
def index(request):
    if request.method == 'GET':
        return render(request, 'Admin/index.html')


# 管理员主界面函数
def test(request):
    if request.method == 'GET':
        return render(request, 'test.html')


# 添加婚纱
def addBv(request):
    if request.method == 'GET':
        return render(request, 'admin/add_bv.html', {'msg': '请认真填写以下信息！'})
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        num = request.POST.get('num').strip()
        price = request.POST.get('price').strip()
        photoMaxNum = request.POST.get('photoMaxNum').strip()
        photoMinNum = request.POST.get('photoMinNum').strip()
        detail = request.POST.get('detail').strip()
        photoImage = request.FILES.get('photoImage')
        print(photoImage, type(photoImage))
        type_list = ['.jpg', '.png']
        # 判断上传图片格式
        imgtype = os.path.splitext(photoImage.name)[1].lower()
        if imgtype not in type_list:
            return render(request, 'admin/add_bv.html', {'msg': '只支持png或者jpg格式的文件！'})
        if int(price) <= 0:
            return render(request, 'admin/add_bv.html', {'msg': '婚纱价格不能小于0！'})
        if int(photoMaxNum) <= 0:
            return render(request, 'admin/add_bv.html', {'msg': '拍摄张数不能小于0！'})
        if int(photoMinNum) <= 0:
            return render(request, 'admin/add_bv.html', {'msg': '可选张数不能小于0！'})
        if int(num) <= 0:
            return render(request, 'admin/add_bv.html', {'msg': '婚纱数量不能小于0！'})
        if len(name) == 0:
            return render(request, 'admin/add_bv.html', {'msg': '婚纱名不能为空！'})
        try:
            bv.objects.get(bv_name=name)
            return render(request, 'admin/add_bv.html', {'msg': '该婚纱名已存在！'})
        except Exception as e:
            print(e)
            try:
                my_bv = bv(bv_name=name, bv_num_all=num, bv_num_now=num, bv_image=photoImage, bv_price=price,
                           bv_photoNumMax=photoMaxNum, bv_photoNumMin=photoMinNum, bv_detail=detail)
                my_bv.save()
                return render(request, 'admin/add_bv.html', {'msg': '添加婚纱成功！'})
            except Exception as e:
                print(e)
                return render(request, 'admin/add_bv.html', {'msg': '添加婚纱失败！'})
        # return render(request, 'admin/add_bv.html')

# 展示婚纱路由
def showBv(request,id):
    pass