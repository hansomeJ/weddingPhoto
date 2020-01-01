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
    return render(request, 'customer/index.html')


def addOrder(request):
    allbv = bv.objects.all()
    allbvs = bvs.objects.all()
    space = Space.objects.all()
    cameraman = Cameraman.objects.all()
    if request.method == 'GET':
        return render(request, 'customer/makeOrder.html',
                      {'msg': '请认真填写以下内容！', 'allBv': allbv, 'allBvs': allbvs, 'space': space, 'cameraman': cameraman})
    else:
        # 男方姓名
        nameOne = request.POST.get('nameOne').strip()
        # 女方姓名
        nameTwo = request.POST.get('nameTwo').strip()
        # 客户电话
        phoneNum = request.POST.get('phoneNum').strip()
        # 预定拍照时间
        myTime = request.POST.get('time').strip()
        myTime = datetime.datetime.strptime(myTime, '%Y-%m-%d %H:%M:%S')
        print(myTime, type(myTime))
        # 婚纱 bv or婚纱组 bvs
        inlineRadioOptions = request.POST.get('inlineRadioOptions').strip()
        # 婚纱
        bv1 = request.POST.get('select1').strip()
        bv2 = request.POST.get('select2').strip()
        bv3 = request.POST.get('select3').strip()
        bv4 = request.POST.get('select4').strip()
        # 婚纱组
        myBvs = request.POST.get('bvs').strip()
        myBvs = bvs.objects.get(pk=myBvs)
        # 场地
        mySpace = request.POST.get('space').strip()
        mySpace = Space.objects.get(pk=mySpace)
        # 摄影师
        cameraMan = request.POST.get('cameraman').strip()
        cameraMan = Cameraman.objects.get(pk=cameraMan)

        # try:
        #     s=order.order_starTime
        #     print(s,type(s))
        # except Exception as e:
        #     print(e)
        if inlineRadioOptions == 'bv':
            order = Order.objects.create(order_nameOne=nameOne, order_nameTwo=nameTwo, order_phoneNum=phoneNum,
                                         order_space=mySpace, order_cameraman=cameraMan, order_photographTime=myTime)
            bvSet = bv.objects.filter(Q(pk=bv1) | Q(pk=bv2) | Q(pk=bv3) | Q(pk=bv4))
            price = 0
            for i in bvSet:
                price += i.bv_price

            # bvS = bvs.objects.create(bvs_name=name, bvs_prices=price)
            order.order_bv.add(*bvSet)
            order.order_moneyNum = price
            try:
                order.save()
                return render(request, 'customer/makeOrder.html',
                              {'msg': '添加订单成功！', 'allBv': allbv, 'allBvs': allbvs, 'space': space,
                               'cameraman': cameraman})
            except Exception as e:
                print(e)
                return render(request, 'customer/makeOrder.html',
                              {'msg': '添加订单失败！', 'allBv': allbv, 'allBvs': allbvs, 'space': space,
                               'cameraman': cameraman})
        else:
            order = Order(order_nameOne=nameOne, order_nameTwo=nameTwo, order_phoneNum=phoneNum,
                          order_space=mySpace, order_cameraman=cameraMan, order_photographTime=myTime)
            order.order_bvs = myBvs
            order.order_moneyNum = myBvs.bvs_prices
            try:
                order.save()
                return render(request, 'customer/makeOrder.html',
                              {'msg': '添加订单成功！', 'allBv': allbv, 'allBvs': allbvs, 'space': space,
                               'cameraman': cameraman})
            except Exception as e:
                print(e)
                return render(request, 'customer/makeOrder.html',
                              {'msg': '添加订单失败！', 'allBv': allbv, 'allBvs': allbvs, 'space': space,
                               'cameraman': cameraman})


def showOrder(request, id, type):
    if type == 'all':
        all = Order.objects.all()
        return render(request, 'customer/showOrders.html', {'order': all})
    elif type == 'ptoto':
        all = Order.objects.filter(order_status='待拍摄')
        return render(request, 'customer/showOrders.html', {'order': all})
    elif type == 'get':
        all = Order.objects.filter(order_status='待取片')
        return render(request, 'customer/showOrders.html', {'order': all})
    elif type == 'comment':
        all = Order.objects.filter(order_status='待评价')
        return render(request, 'customer/showOrders.html', {'order': all})
    else:
        order = Order.objects.get(pk=id)
        return render(request, 'customer/showOrder.html', {'order': order})
