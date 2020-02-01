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
from weddingPhotoMS import utils
from django.db.models import Q
from weddingPhotoMS.utils import create_code, pwd_by_hashlib, pwd_by_hmac


def addComment(request, id):
    name = request.session['login_user']['name']
    user = Customer.objects.get(cs_name=name)
    order = Order.objects.get(pk=id, order_owner=user)
    if request.method == 'GET':
        return render(request, 'comment/addComment.html', {'order': order})
    else:
        bv1 = request.POST.get('bv1', None)
        bv2 = request.POST.get('bv2', None)
        bv3 = request.POST.get('bv3', None)
        bv4 = request.POST.get('bv4', None)
        bvs = request.POST.get('bvs', None)
        space = request.POST.get('space', None)
        cameraman = request.POST.get('cameraman', None)
        try:
            # print(dir(order.order_bv.all()),type(order.order_bv.all()),order.order_bv.all())
            # for i in order.order_bv.all():
            #     print(i)
            if bv1 is not None:
                bv1_comment = Comment_Bv(order=order, c_bvId=order.order_bv.all()[0], c_customerId=user, c_content=bv1)
                bv2_comment = Comment_Bv(order=order, c_bvId=order.order_bv.all()[1], c_customerId=user, c_content=bv2)
                bv3_comment = Comment_Bv(order=order, c_bvId=order.order_bv.all()[2], c_customerId=user, c_content=bv3)
                bv4_comment = Comment_Bv(order=order, c_bvId=order.order_bv.all()[3], c_customerId=user, c_content=bv4)
                bv1_comment.save()
                bv2_comment.save()
                bv3_comment.save()
                bv4_comment.save()
            if bvs is not None:
                bvs_comment = Comment_Bvs(order=order, c_bvs=order.order_bvs, c_customer=user, c_content=bvs)
                bvs_comment.save()
            space_comment = Comment_Space(order=order, c_spaceId=order.order_space, c_customerId=user, c_content=space)
            space_comment.save()
            cameraman_comment = Comment_Camerman(order=order, c_cameraman=order.order_cameraman, c_customer=user,
                                                 c_content=cameraman)
            cameraman_comment.save()
            order.order_status = '已完成'
            order.order_endTime = utils.nowTime()
            order.save()
            return render(request, 'comment/addComment.html', {'order': order, 'msg': '评论成功！'})
        except Exception as e:
            print(e)
            return render(request, 'comment/addComment.html', {'order': order, 'msg': '评论失败！'})


def showComment(request):
    name = request.session['login_user']['name']
    user = Customer.objects.get(cs_name=name)
    # order = Order.objects.get(pk=id, order_owner=user)
    bv_comments = Comment_Bv.objects.filter(c_customerId=user)
    bvs_comments = Comment_Bvs.objects.filter(c_customer=user)
    cameraman_comments = Comment_Camerman.objects.filter(c_customer=user)
    space_comments = Comment_Space.objects.filter(c_customerId=user)
    return render(request, 'customer/showcomment.html',
                  {'bv': bv_comments, 'bvs': bvs_comments, 'cameraman': cameraman_comments, 'space': space_comments})
