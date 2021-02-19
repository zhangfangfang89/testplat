from django.http import JsonResponse
from rest_framework.views import APIView

from web.models import ApiInfo, ProjectInfo


class ApiListViewAll(APIView):
    """查询db"""

    def get(self, request):
        query = ApiInfo.objects.all()

        dataList = query.values("name")

        return JsonResponse({'code': 20000, 'message': "success", 'data': {"items": list(dataList)}})


class ApiListView(APIView):
    """查询数据"""

    def get(self, request):
        name = request.GET.get("name")

        page = int(request.GET.get("page"))
        limit = int(request.GET.get("limit"))
        query = ApiInfo.objects.all();
        if name:
            query = query.filter(name__contains=name)
        dataList = query.values("id", "name", "plat", "uil", "headers", "payload")
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


class AddApiView(APIView):

    def post(self, request):
        name = request.data.get('name')
        plat = request.data.get('plat')

        uil = request.data.get('uil')
        headers = request.data.get('headers')
        payload = request.data.get('payload')

        info = ApiInfo.objects.filter(name=name).exists()

        if info:
            return JsonResponse({"code": 50000, "message": "该别名的配置已存在"})

        ApiInfo.objects.create(name=name, plat=plat, uil=uil, headers=headers, payload=payload)
        info = ApiInfo.objects.filter(name=name).values("id", "name", "plat", "uil", "headers", "payload")
        print(info)
        return JsonResponse({"code": 20000, "data": list(info), "message": "添加成功"})


class DeleteApiView(APIView):
    def post(self, request):
        info = ApiInfo.objects.get(id=request.data.get('id'))

        if not ProjectInfo.objects.filter(plat=info).exists():
            info.delete()
            return JsonResponse({"code": 20000, "message": "删除成功"})
        return JsonResponse({"code": 50000, "message": "该数据被使用不可删除，请尝试修改"})


class UpdateApiView(APIView):
    def post(self, request):
        id = request.data.get('id')
        name = request.data.get("name")
        plat = request.data.get('plat')
        uil = request.data.get('uil')
        headers = request.data.get('headers')
        payload = request.data.get('payload')
        info = ApiInfo.objects

        info.filter(name=name).update(uil=uil, plat=plat, headers=headers, payload=payload)

        info = ApiInfo.objects.filter(name=name).values("id", 'name', "plat", "uil", "headers", "payload")

        return JsonResponse({"code": 20000, "data": list(info), "message": "编辑成功"})
