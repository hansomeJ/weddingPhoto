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
from comment.models import Comment_Bv
from comment.models import Comment_Bvs
from comment.models import Comment_Space
from comment.models import Comment_Camerman
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


def updateMsg(request):
    name = request.session['login_cameraman']['name']
    user = Cameraman.objects.get(ca_name=name)
    if request.method == 'GET':
        return render(request, 'cameraman/updateMsg.html', {"ca": user})
    else:
        nickName = request.POST.get('name')
        detail = request.POST.get('detail')
        gender = request.POST.get('gender')
        image = request.FILES.get('photoImage')
        type_list = ['.jpg', '.png']
        # 判断上传图片格式
        imgtype = os.path.splitext(image.name)[1].lower()
        if imgtype not in type_list:
            return render(request, 'cameraman/updateMsg.html', {"ca": user, 'msg': '只支持png或者jpg格式的文件！'})

        try:
            user.ca_nickName = nickName
            user.ca_detail = detail
            user.ca_gender = gender
            os.remove(str(user.ca_image))
            user.ca_image = image
            user.save()
            return render(request, 'cameraman/updateMsg.html', {"ca": user, 'msg': '修改信息成功！'})
        except Exception as e:
            print(e)
            return render(request, 'cameraman/updateMsg.html', {"ca": user, 'msg': '修改信息失败！'})


def showOrder(request, id, type):
    ca_name = request.session['login_cameraman']['name']
    user = Cameraman.objects.get(ca_name=ca_name)
    if type == 'all':
        all = Order.objects.filter(order_cameraman=user)
        return render(request, 'cameraman/showOrders.html', {'order': all})
    elif type == 'photo':
        all = Order.objects.filter(order_cameraman=user, order_status='待拍摄')
        return render(request, 'cameraman/showOrders.html', {'order': all})
    elif type == 'get':
        all = Order.objects.filter(order_cameraman=user, order_status='待取片')
        return render(request, 'cameraman/showOrders.html', {'order': all})
    elif type == 'comment':
        all = Order.objects.filter(order_cameraman=user, order_status='待评价')
        return render(request, 'cameraman/showOrders.html', {'order': all})
    elif type == 'end':
        all = Order.objects.filter(order_cameraman=user, order_status='已完成')
        return render(request, 'cameraman/showOrders.html', {'order': all})
    else:
        order = Order.objects.get(order_cameraman=user, pk=id)
        return render(request, 'cameraman/showOrder.html', {'order': order})


def updateOrder(request, id):
    order = Order.objects.get(pk=id)
    if request.method == 'POST':
        selectTime = request.POST.get('selectTime', None)
        getTime = request.POST.get('getTime', None)
        print(selectTime, getTime)
        if selectTime != None:
            try:
                order.order_selectTime = selectTime
                order.order_status = '待取片'
                order.save()
                return render(request, 'cameraman/showOrder.html', {'order': order})
            except Exception as e:
                print(e)
                return render(request, 'cameraman/showOrder.html', {'order': order, 'msg': '修改失败'})
        if getTime != None:
            try:
                order.order_getTime = getTime
                order.order_status = '待评价'
                order.save()
                return render(request, 'cameraman/showOrder.html', {'order': order})
            except Exception as e:
                print(e)
                return render(request, 'cameraman/showOrder.html', {'order': order, 'msg': '修改失败'})


def showComment(request):
    name = request.session['login_cameraman']['name']
    user = Cameraman.objects.get(ca_name=name)
    # order = Order.objects.get(pk=id, order_owner=user)
    cameraman_comments = Comment_Camerman.objects.filter(c_cameraman=user)
    return render(request, 'cameraman/showcomment.html',
                  {'cameraman': cameraman_comments})
