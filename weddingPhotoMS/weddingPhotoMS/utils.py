import hashlib
import hmac
import random
import string
from PIL import Image,ImageDraw,ImageFont,ImageFilter


from django.shortcuts import render
from django.conf import settings

from datetime import datetime

def nowTime():
    t = str(datetime.now())
    t1 = t.split('.')
    t2 = str(t1[0])
    return t2

def get_random_char(count=4):
    # 生成随机字符串
    # string模块包含各种字符串，以下为小写字母加数字
    ran = string.ascii_lowercase + string.ascii_uppercase + string.digits
    char = ''
    for i in range(count):
        char += random.choice(ran)
    return char


def get_random_color():
    # 返回一个随机的RGB颜色
    return random.randint(200,255), random.randint(200,255), random.randint(200,255)


def create_code():
    # 创建图片，模式，大小，背景色
    img = Image.new('RGB', (120,30), (94,86,125))
    #创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype('arial.ttf', 25)

    code = get_random_char()
    # 将生成的字符画在画布上
    for t in range(4):
        draw.text((30*t+5,0),code[t],get_random_color(),font)

    # 生成干扰点
    for _ in range(random.randint(0,50)):
        # 位置，颜色
        draw.point((random.randint(0, 120), random.randint(0, 30)),fill=get_random_color())

    # 使用模糊滤镜使图片模糊
    # img = img.filter(ImageFilter.BLUR)
    # 保存
    # img.save(''.join(code)+'.jpg','jpeg')
    return img, code






def require_login_user(fn):
    """
    一个判断用户是否登录的装饰器
    :param fn: 视图函数
    :return: 如果已经登录，则进入视图函数，如果没有登录，则返回登录页面
    """
    def inner(request, *args, **kwargs):
        # 判断session是否存在登录用户
        login_user = request.session.get("login_user", None)
        if login_user is not None:
            return fn(request, *args, **kwargs)
        else:
            # 将页面打到登录页面
            return render(request, "customer/login.html", {"msg": "对不起，该页面必须登录才能访问"})

    return inner

def require_login_admin(fn):
    """
    一个判断用户是否登录的装饰器
    :param fn: 视图函数
    :return: 如果已经登录，则进入视图函数，如果没有登录，则返回登录页面
    """
    def inner(request, *args, **kwargs):
        # 判断session是否存在登录用户
        login_admin = request.session.get("login_admin", None)
        if login_admin is not None:
            return fn(request, *args, **kwargs)
        else:
            # 将页面打到登录页面
            return render(request, "_admin/login.html", {"msg": "对不起，该页面必须登录才能访问"})
    return inner

def require_login_type1(fn):
    """
    一个判断用户是否登录的装饰器
    :param fn: 视图函数
    :return: 如果已经登录，则进入视图函数，如果没有登录，则返回登录页面
    """
    def inner(request, *args, **kwargs):
        # 判断session是否存在登录用户
        login_admin = request.session.get("login_admin", None)
        if login_admin == None:
            return render(request, "_admin/login.html", {"msg": "对不起，该页面只能平台管理员访问"})
        if login_admin.type =='平台管理员':
            return fn(request, *args, **kwargs)
        else:
            # 将页面打到登录页面
            return render(request, "_admin/login.html", {"msg": "对不起，该页面只能平台管理员访问"})
    return inner


def require_login_type2(fn):
    """
    一个判断用户是否登录的装饰器
    :param fn: 视图函数
    :return: 如果已经登录，则进入视图函数，如果没有登录，则返回登录页面
    """

    def inner(request, *args, **kwargs):
        # 判断session是否存在登录用户
        login_admin = request.session.get("login_admin", None)
        if login_admin == None:
            return render(request, "_admin/login.html", {"msg": "对不起，该页面只能订单管理员访问"})
        if login_admin.type == '订单管理员' :
            return fn(request, *args, **kwargs)
        else:
            # 将页面打到登录页面
            return render(request, "_admin/login.html", {"msg": "对不起，该页面只能订单管理员访问"})

    return inner


def require_login_type3(fn):
    """
    一个判断用户是否登录的装饰器
    :param fn: 视图函数
    :return: 如果已经登录，则进入视图函数，如果没有登录，则返回登录页面
    """

    def inner(request, *args, **kwargs):
        # 判断session是否存在登录用户
        login_admin = request.session.get("login_admin", None)
        if login_admin == None:
            return render(request, "_admin/login.html", {"msg": "对不起，该页面只能快递员访问"})
        if login_admin.type == '快递员':
            return fn(request, *args, **kwargs)
        else:
            # 将页面打到登录页面
            return render(request, "_admin/login.html", {"msg": "对不起，该页面只能快递员访问"})

    return inner
def pwd_by_hashlib(password,i=100):
    """
    使用hashlib模块完成对用户密码的加密
    :param password: 用户密码
    :return: 一个加密后密文
    """
    md5 = hashlib.md5(password.encode("utf-8"))
    md5.update(settings.SECRET_KEY.encode("utf-8"))
    if i>=0:
        i-=1
        pwd_by_hashlib(md5.hexdigest(),i)
        # print(md5.hexdigest(),i)
    else:
        return md5.hexdigest()


def pwd_by_hmac(password):
    """
    使用hmac模块完成对用户密码的加密
    :param password: 用户密码
    :return: 一个加密后密文
    """
    return hmac.new(settings.SECRET_KEY.encode("utf-8"),
                    password.encode("utf-8"),
                    "MD5").hexdigest()


# if __name__ == '__main__':
#     # pwd_by_hashlib('123456')
#     # print(create_code())




