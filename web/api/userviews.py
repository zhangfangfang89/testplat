import hashlib

from django.http import JsonResponse
from rest_framework.views import APIView

from web.models import UserToken, UserInfo


def tokenMd5(pw):
    password = hashlib.md5()
    password.update(pw.encode("utf-8"))
    return password.hexdigest()


class LoginView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if username and password:
            user_instance = UserInfo.objects.filter(mobile=username, password=password).first()
            print(user_instance)
            if user_instance:
                user_token = username + "." + tokenMd5(password)
                user_token = UserToken.objects.create(user=user_instance, token=user_token)
                return JsonResponse({'code': 20000, 'data': {'token': user_token.token}})
            # return HttpResponse(json.loads("{'code':20000,'data':{'token':{}}}".format(token)))
        return JsonResponse({"code": 60204, 'message': 'Account and password are incorrect.'})


class UserInfoView(APIView):

    def get(self, request):
        token = request.META.get('QUERY_STRING')
        print(token)
        mobile = token.split("=")[1].split('.')[0]
        print(mobile)
        usename = UserInfo.objects.get(mobile=mobile).username
        print(usename)
        return JsonResponse({"code": 20000, "data": {"roles": [usename], "introduction": "I am {}".format(usename),
                                                     "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                                                     "name": usename}})


class LogoutView(APIView):
    def post(self, request):
        return JsonResponse({'code': 20000, 'data': 'success'})


class UsermanageView(APIView):
    # 查询用户
    def get(self, request):
        mobile = request.GET.get("mobile")
        page = int(request.GET.get("page"))
        limit = int(request.GET.get("limit"))
        query = UserInfo.objects.all();
        if mobile:
            query = query.filter(mobile=mobile)
        dataList = query.values('id', 'username', 'mobile')
        count = dataList.count()
        if page * limit < count:
            dataList = list(dataList)[(page - 1) * limit:page * limit]
            print(dataList)
            print(len(dataList))
        else:
            dataList = list(dataList)[(page - 1) * limit:count]
            print(dataList)
            print(len(dataList))
        return JsonResponse({'code': 20000, 'message': "success", 'data': {"items": list(dataList), 'total': count}})

    # 添加用户
    def post(self, request):
        username = request.data.get('username')
        mobile = request.data.get('mobile')
        password = request.data.get('password')
        useinfo = UserInfo.objects.filter(mobile=mobile).exists()
        if useinfo:
            return JsonResponse({"code": 50000, "message": "电话已经存在"})

        if len(str(mobile)) < 11 or (not mobile.isdigit()):
            return JsonResponse({"code": 50000, "message": "电话格式不正确"})

        UserInfo.objects.create(username=username, mobile=mobile, password=password)
        useinfo = UserInfo.objects.filter(mobile=mobile).values("id", "username", "mobile")
        print(useinfo)
        return JsonResponse({"code": 20000, "data": list(useinfo), "message": "添加成功"})


# 删除用户
class DeleteUserView(APIView):
    def post(self, request):
        userinfo = UserInfo.objects.get(id=request.data.get('id'))
        userinfo.delete()
        return JsonResponse({"code": 20000, "message": "删除成功"})
