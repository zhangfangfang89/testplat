from django.http import JsonResponse
from rest_framework.views import APIView

from web.models import DbInfo, ProjectInfo


class DbListViewAll(APIView):
    """查询db"""

    def get(self, request):
        query = DbInfo.objects.all()

        dataList = query.values("name")

        return JsonResponse({'code': 20000, 'message': "success", 'data': {"items": list(dataList)}})


class DbListView(APIView):
    """查询db"""

    def get(self, request):
        name = request.GET.get("name")
        page = int(request.GET.get("page"))
        limit = int(request.GET.get("limit"))
        query = DbInfo.objects.all()
        if name:
            query = query.filter(name__contains=name)
        dataList = query.values("id", "name", "ip", "port", "database", "username", "password")
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


class AddDbView(APIView):

    # 添加用户
    def post(self, request):
        name = request.data.get('name')
        ip = request.data.get('ip')
        port = request.data.get('port')
        username = request.data.get('username')
        database = request.data.get('database')
        password = request.data.get('password')
        if not (name.isalpha() or name.isdigit()):
            return JsonResponse({"code": 50000, "message": "别名为字母或者数字组成"})
        dbinfo = DbInfo.objects.filter(name=name).exists()
        if dbinfo:
            return JsonResponse({"code": 50000, "message": "该别名的配置已存在"})

        DbInfo.objects.create(name=name, ip=ip, port=port, username=username, database=database, password=password)
        dbinfo = DbInfo.objects.filter(name=name).values("id", "name", "ip", "port", "database", "username",
                                                         "password")
        print(dbinfo)
        return JsonResponse({"code": 20000, "data": list(dbinfo), "message": "添加成功"})


# 删除用户
class DeleteDbView(APIView):
    def post(self, request):
        dbinfo = DbInfo.objects.get(id=request.data.get('id'))
        print(dbinfo)
        if not ProjectInfo.objects.filter(db=dbinfo).exists():
            dbinfo.delete()
            return JsonResponse({"code": 20000, "message": "删除成功"})
        return JsonResponse({"code": 50000, "message": "该数据被使用不可删除，请尝试修改"})


class UpdateDbView(APIView):
    def post(self, request):
        id = request.data.get('id')
        name = request.data.get('name')
        ip = request.data.get('ip')
        port = request.data.get('port')
        username = request.data.get('username')
        database = request.data.get('database')
        password = request.data.get('password')
        dbinfo = DbInfo.objects
        if dbinfo.get(id=id).name != name:
            return JsonResponse({"code": 50000, "message": "别名字段不可修改"})
        dbinfo.filter(name=name).update(ip=ip, port=port, username=username, database=database, password=password)

        dbinfo = DbInfo.objects.filter(name=name).values("id", "name", "ip", "port", "database", "username",
                                                         "password")
        print(dbinfo)
        return JsonResponse({"code": 20000, "data": list(dbinfo), "message": "编辑成功"})
