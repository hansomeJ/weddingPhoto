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
                request.session.set_expiry(0)
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
                request.session.set_expiry(0)
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
                request.session.set_expiry(0)
                result = {'Success': True}
                return JsonResponse(result)
        except Exception as e:
            # 该用户不存在
            print(e)
            return JsonResponse({'Failed': True})


# 管理员主界面函数
def index(request):
    space = Space.objects.all().order_by('-s_sale_num')[:3]
    print(space)
    if request.method == 'GET':
        return render(request, 'Admin/index.html', {'space': space})


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
        if int(photoMinNum) > int(photoMaxNum):
            return render(request, 'admin/updateBv.html', {'msg': '可选张数不能大于拍摄张数！'})
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
def showBv(request, id):
    if request.method == 'GET' and id == '0':
        allBv = bv.objects.all()
        # print(dir(allBv[0]))
        return render(request, 'admin/showAllBv.html', {'allBv': allBv})


def updateBv(request, id):
    targetBv = bv.objects.get(pk=id)
    if request.method == 'GET':
        return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '请修改下面信息！'})
    else:
        name = request.POST.get('name').strip()
        numAll = request.POST.get('numAll').strip()
        numNow = request.POST.get('numNow').strip()
        price = request.POST.get('price').strip()
        photoMaxNum = request.POST.get('photoMaxNum').strip()
        photoMinNum = request.POST.get('photoMinNum').strip()
        detail = request.POST.get('detail').strip()
        photoImage = request.FILES.get('photoImage')
        type_list = ['.jpg', '.png']

        if int(price) <= 0:
            return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '婚纱价格不能小于0！'})
        if int(photoMaxNum) <= 0:
            return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '拍摄张数不能小于0！'})
        if int(photoMinNum) <= 0:
            return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '可选张数不能小于0！'})
        if int(photoMinNum) > int(photoMaxNum):
            return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '可选张数不能大于拍摄张数！'})
        if int(numAll) <= 0:
            return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '婚纱数量不能小于0！'})
        if int(numNow) < 0:
            return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '婚纱数量不能小于0！'})
        if int(numNow) > int(numAll):
            return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '当前数量不能大于总数量'})
        if len(name) == 0:
            return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '婚纱名不能为空！'})
        targetBv.bv_name = name
        targetBv.bv_num_all = numAll
        targetBv.bv_num_now = numNow
        targetBv.bv_photoNumMax = photoMaxNum
        targetBv.bv_photoNumMin = photoMinNum
        targetBv.bv_detail = detail
        if photoImage != None:
            imgtype = os.path.splitext(photoImage.name)[1].lower()
            if imgtype not in type_list:
                return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '只支持png或者jpg格式的文件！'})
            try:
                # print(targetBv.bv_image,type(str(targetBv.bv_image)))
                os.remove(str(targetBv.bv_image))
                targetBv.bv_image = photoImage
                targetBv.save()
                return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '修改婚纱信息成功！'})
            except Exception as e:
                print(e)
                return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '修改婚纱信息失败！'})
        else:
            try:
                targetBv.save()
                return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '修改婚纱信息成功！'})
            except Exception as e:
                print(e)
                return render(request, 'admin/updateBv.html', {'bv': targetBv, 'msg': '修改婚纱信息失败！'})


def deleteBv(request, id):
    targetBv = bv.objects.get(pk=id)
    allBv = bv.objects.all()
    try:
        targetBv.bridal_veils_set.clear()
        targetBv.order_set.clear()
        os.remove(str(targetBv.bv_image))
        targetBv.delete()
        return render(request, 'admin/showAllBv.html', {'allBv': allBv})
    except Exception as e:
        print(e)
        return render(request, 'admin/showAllBv.html', {'allBv': allBv})


# 添加婚纱组
def addBvs(request):
    allBv = bv.objects.all()
    if request.method == 'GET':
        return render(request, 'admin/add_bvs.html', {'allBv': allBv, 'msg': '请填写以下信息！'})
    else:
        name = request.POST.get('name').strip()
        bv1 = request.POST.get('select1')
        bv2 = request.POST.get('select2')
        bv3 = request.POST.get('select3')
        bv4 = request.POST.get('select4')
        bv_set = {bv1, bv2, bv3, bv4}
        try:
            bvs.objects.get(bvs_name=name)
            return render(request, 'admin/add_bvs.html', {'allBv': allBv, 'msg': '该组名已存在不能重复添加！'})
        except:
            if name == '':
                return render(request, 'admin/add_bvs.html', {'allBv': allBv, 'msg': '组名不能为空！'})
            if len(bv_set) != 4:
                return render(request, 'admin/add_bvs.html', {'allBv': allBv, 'msg': '不能选择相同的婚纱！'})
            else:
                # bvOne = bv.objects.get(pk=bv1)
                # bvTwo = bv.objects.get(pk=bv2)
                # bvThree = bv.objects.get(pk=bv3)
                # bvFour = bv.objects.get(pk=bv4)
                try:
                    bvSet = bv.objects.filter(Q(pk=bv1) | Q(pk=bv2) | Q(pk=bv3) | Q(pk=bv4))
                    price = 0
                    for i in bvSet:
                        price += i.bv_price

                    bvS = bvs.objects.create(bvs_name=name, bvs_prices=price)
                    bvS.bvs_bv.add(*bvSet)
                    bvS.save()
                    return render(request, 'admin/add_bvs.html', {'allBv': allBv, 'msg': '添加成功！'})
                except Exception as e:
                    print(e)
                    return render(request, 'admin/add_bvs.html', {'allBv': allBv, 'msg': '添加失败！'})


# 展示婚纱组
def showBvs(request):
    if request.method == 'GET':
        allBvs = bvs.objects.all().order_by('-bvs_sale_num')
        # print(allBvs)

        for bv in allBvs:
            s = bv.bvs_bv.all()
            # print(s)

        return render(request, 'admin/showAllBvs.html', {'allBvs': allBvs})


# 删除婚纱组
def deleteBvs(request, id):
    targetBvs = bvs.objects.get(pk=id)
    allBvs = bvs.objects.all()
    try:
        targetBvs.bvs_bv.clear()
        targetBvs.delete()
        return render(request, 'admin/showAllBvs.html', {'allBvs': allBvs})
    except Exception as e:
        print(e)
        return render(request, 'admin/showAllBvs.html', {'allBvs': allBvs})


def addSpace(request):
    if request.method == 'GET':
        return render(request, 'admin/addSpace.html', {'msg': '请填写以下信息！'})
    else:
        name = request.POST.get('name').strip()
        detail = request.POST.get('detail').strip()
        Image = request.FILES.get('Image')
        try:
            Space.objects.get(s_name=name)
            return render(request, 'admin/addSpace.html', {'msg': '该场地名已存在不能重复添加！'})
        except:
            if detail == '':
                return render(request, 'admin/addSpace.html', {'msg': '简介不能为空！'})
            if name == '':
                return render(request, 'admin/addSpace.html', {'msg': '场地名不能为空！'})
            type_list = ['.jpg', '.png']
            # 判断上传图片格式
            imgtype = os.path.splitext(Image.name)[1].lower()
            if imgtype not in type_list:
                return render(request, 'admin/addSpace.html', {'msg': '只支持png或者jpg格式的文件！'})
            try:
                Space.objects.get(s_name=name)
                return render(request, 'admin/addSpace.html', {'msg': '该场地名已存在！'})
            except Exception as e:
                print(e)
                try:
                    tarSpace = Space(s_name=name, s_image=Image, s_detail=detail)
                    tarSpace.save()
                    return render(request, 'admin/addSpace.html', {'msg': '添加场地成功！'})
                except Exception as e:
                    print(e)
                    return render(request, 'admin/addSpace.html', {'msg': '添加场地失败！'})


# 显示所有场地函数
def showSpace(request):
    if request.method == 'GET':
        space = Space.objects.all()
        return render(request, 'admin/showAllSpace.html', {'space': space})


# 删除场地函数
def deleteSpace(request, id):
    space = Space.objects.all()
    targetSpace = Space.objects.get(pk=id)
    if request.method == 'GET':
        try:
            targetSpace.order_set.clear()
            os.remove(str(targetSpace.s_image))
            targetSpace.delete()
            return render(request, 'admin/showAllSpace.html', {'space': space})
        except Exception as e:
            print(e)
            return render(request, 'admin/showAllSpace.html', {'space': space})


# 更新场地信息函数
def updateSpace(request, id):
    targetSpace = Space.objects.get(pk=id)
    if request.method == 'GET':
        return render(request, 'admin/updateSpace.html', {'msg': '请填写以下信息！', 's': targetSpace})
    else:
        name = request.POST.get('name').strip()
        detail = request.POST.get('detail').strip()
        Image = request.FILES.get('Image')
        print(Image)
        if detail == '':
            return render(request, 'admin/updateSpace.html', {'msg': '简介不能为空！', 's': targetSpace})
        if name == '':
            return render(request, 'admin/updateSpace.html', {'msg': '场地名不能为空！', 's': targetSpace})
        targetSpace.s_name = name
        targetSpace.s_detail = detail
        if Image != None:
            type_list = ['.jpg', '.png']
            # 判断上传图片格式
            imgtype = os.path.splitext(Image.name)[1].lower()
            if imgtype not in type_list:
                return render(request, 'admin/updateSpace.html', {'msg': '只支持png或者jpg格式的文件！', 's': targetSpace})
            try:
                os.remove(str(targetSpace.s_image))
                targetSpace.s_image = Image
                targetSpace.save()
                return render(request, 'admin/updateSpace.html', {'msg': '修改成功！', 's': targetSpace})
            except Exception as e:
                print(e)
                return render(request, 'admin/updateSpace.html', {'msg': '修改场地失败！', 's': targetSpace})
        else:
            try:
                targetSpace.save()
                return render(request, 'admin/updateSpace.html', {'msg': '修改成功！', 's': targetSpace})
            except Exception as e:
                print(e)
                return render(request, 'admin/updateSpace.html', {'msg': '修改场地失败！', 's': targetSpace})


# 发布公告
def notice(request):
    if request.method == 'GET':
        return render(request, 'admin/notice.html')
    else:
        title = request.POST.get('title').strip()
        content = request.POST.get('content').strip()
        if title == '':
            return render(request, 'admin/notice.html', {"msg": '公告标题不能为空！'})
        if content == '':
            return render(request, 'admin/notice.html', {"msg": '公告内容不能为空！'})
        notice = Notice(notice_title=title, notice_content=content)
        try:
            notice.save()
            return render(request, 'admin/notice.html', {"msg": '发布公告成功！'})
        except Exception as e:
            print(e)
            return render(request, 'admin/notice.html', {"msg": '发布公告失败！'})


# 查看公告
def noticeShow(request):
    notice = Notice.objects.all().order_by('-notice_time')[0]
    return render(request, 'admin/showNotice.html', {"n": notice})

# 退出登录
def logout(request):
    request.session.clear()
    return redirect(r'http://127.0.0.1:8000')