import os, sys, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf.settings")
django.setup()
from django.http import JsonResponse
from rest_framework.views import APIView

from web.models import ProjectInfo, DbInfo, ApiInfo, ApiManage

from django.conf import settings
from tools.log_tool import Logger

from tools.configparser_tool import ConfigparserUse
from django.db import transaction
import ast

# 生成项目和配置文件

def makeProject(project_name):
    dir_project = settings.BASE_DIR
    dir_venv = os.path.join(dir_project, "venv")
    # 创建项目
    try:
        result = os.system('cd {} && ./makeproject.sh {} {}'.format(dir_project, dir_venv, project_name))
        print(result)
        if result == 0:
            settings.INSTALLED_APPS.append(project_name)

        else:
            logger = Logger(os.path.join(dir_project, "log"))
            l = logger.rotateInputLog()
            l.debug("创建项目失败")
    except Exception as e:
        logger = Logger(os.path.join(dir_project, "log"))
        l = logger.rotateInputLog()
        l.debug("创建项目失败")
        print("创建项目失败")


class ProjectListViewAll(APIView):

    def get(self, request):
        query = ProjectInfo.objects.all()

        dataList = query.values("name")

        return JsonResponse({'code': 20000, 'message': "success", 'data': {"items": list(dataList)}})
class ModuleListView(APIView):
    def get(self,request):
        list_module = []

        project = request.GET.get('0')
        print(project)
        module = ProjectInfo.objects.get(name=project).module
        if module :
          for key, value in ast.literal_eval(module).items():
              list_module.append({"name":value})
        return JsonResponse({"code":20000,"data":list_module})

class ProjectListView(APIView):
    """查询数据"""

    def get(self, request):
        name = request.GET.get("name")
        page = int(request.GET.get("page"))
        limit = int(request.GET.get("limit"))
        query = ProjectInfo.objects.all()
        if name:
            query = query.filter(name__contains=name)

        dataList = list(query.values("id", "name", "alias","module", "dec", 'db', "plat"))
        count = len(dataList)
        if page * limit < count:
            dataList = list(dataList)[(page - 1) * limit:page * limit]
        else:
            dataList = list(dataList)[(page - 1) * limit:count]
        return JsonResponse({'code': 20000, 'message': "success", 'data': {"items": dataList, 'total': count}})


class AddProjectView(APIView):

    def post(self, request):
        name = request.data.get('name')
        alias = request.data.get("alias")
        dec = request.data.get('dec')
        db_name = request.data.get('db')
        api_name = request.data.get('plat')
        module = request.data.get('module')
        dbinfo = DbInfo.objects.get(name=db_name)
        typeinfo = ApiInfo.objects.get(name=api_name)
        try:
            with transaction.atomic():

                if not (alias.isalpha() or alias.isdigit()):
                    return JsonResponse({"code": 50000, "message": "别名要为字母或者数字组成"})
                projectinfo = ProjectInfo.objects.filter(name=name).exists()
                if projectinfo:
                    return JsonResponse({"code": 50000, "message": "该项目已存在"})


                if not isinstance(ast.literal_eval(module),dict):
                    return JsonResponse({"code": 50000, "message": "模块要求输入字典类型"})
                else:
                    for key in ast.literal_eval(module):
                         if not (key.isalpha() or key.isdigit()):
                             return JsonResponse({"code": 50000, "message": "模块要求输入字典的key为字母或者数字的组合"})

                ProjectInfo.objects.create(name=name, alias=alias, dec=dec, db=dbinfo,module=module,plat=typeinfo)
                print(settings.INSTALLED_APPS)
                settings.INSTALLED_APPS.append(str(alias))
                print(settings.INSTALLED_APPS)


        except Exception as e:
            print(e)
            return JsonResponse({"code": 50000, "message": "添加失败"})

        # 返回值拼接

        info = ProjectInfo.objects.filter(name=name).values("id", "name", "alias", "dec",'module', 'db', 'plat')
        dataList = list(info)

        # 设置配置文件

        apibaseinfo = ApiInfo.objects.filter(name=api_name).values("plat", "uil", "headers", "payload")
        dbbaseinfo = DbInfo.objects.filter(name=db_name).values("name", "ip", "port", "database", "username",
                                                                "password")
        makeProject(alias)

        os.system("cd {} && cp ./api/apibase.py ./{}/apibase.py".format(settings.BASE_DIR, alias))
        os.system("cd {} && cp ./api/allapi.py ./{}/singelapi/allapi.py".format(settings.BASE_DIR, alias))
        os.system("cd {} && cp ./api/runapi.py ./{}/singelapi/runapi.py".format(settings.BASE_DIR, alias))

        # 创建模块对应的文件
        for key in ast.literal_eval(module):
            print(key)
        os.system("cd {} && mkdir {}".format(os.path.join(os.path.join(settings.BASE_DIR, alias), 'testcase'),
                                             'test_' + key))
        os.system("cd {1} && cp ./api/case.py ./{2}/testcase/{3}/{3}.py".format(settings.BASE_DIR, alias, 'test_' + key))

        dir_base = os.path.join(os.path.join(os.path.join(settings.BASE_DIR, alias), "config"), "base.ini")
        configer = ConfigparserUse(dir_base)
        # api的公共配置

        session = apibaseinfo[0]["plat"]
        value = apibaseinfo[0]["uil"]
        configer.set_value(session, "uil", value)
        value = apibaseinfo[0]["headers"]
        configer.set_value(session, "headers", value)
        value = apibaseinfo[0]["payload"]
        configer.set_value(session, "payload", value)
        # bd的配置
        session = dbbaseinfo[0]["name"]
        value = dbbaseinfo[0]["ip"]
        configer.set_value(session, "ip", value)
        value = dbbaseinfo[0]["port"]
        configer.set_value(session, "port", value)
        value = dbbaseinfo[0]["database"]
        configer.set_value(session, "database", value)
        value = dbbaseinfo[0]["username"]
        configer.set_value(session, "username", value)
        value = dbbaseinfo[0]["password"]
        configer.set_value(session, "password", value)

        return JsonResponse({"code": 20000, "data": dataList, "message": "添加成功"})


class DeleteProjectView(APIView):
    def post(self, request):
        info = ProjectInfo.objects.get(id=request.data.get('id'))
        alias = info.alias
        if not ApiManage.objects.filter(project=info):
            info.delete()
            dir_base = os.path.join(settings.BASE_DIR, alias)
            result = 1
            while result == 1:
                result = os.system("rm -rf {}".format(dir_base))

            while settings.INSTALLED_APPS.__contains__(alias):
                settings.INSTALLED_APPS.remove(alias)

            return JsonResponse({"code": 20000, "message": "删除成功"})
        return JsonResponse({"code": 50000, "message": "该项目已经存在接口数据，不可以删除"})


class UpdateProjectView(APIView):
    def post(self, request):
        name = request.data.get('name')
        db = request.data.get('db')
        dec = request.data.get('dec')
        plat = request.data.get('plat')
        module = request.data.get('module')
        info = ProjectInfo.objects.filter(name=name)[0]
        module_before = info.module

        if not isinstance(ast.literal_eval(module), dict):
            return JsonResponse({"code": 50000, "message": "模块要求输入字典类型"})
        else:
            for key in ast.literal_eval(module):
                if not (key.isalpha() or key.isdigit()):
                    return JsonResponse({"code": 50000, "message": "模块要求输入字典的key为字母或者数字的组合"})

        ProjectInfo.objects.filter(name=name).update(dec=dec, db=db, plat=plat,module=module)
        alias = ProjectInfo.objects.filter(name=name)[0].alias
        for key in ast.literal_eval(module):
            if key not in ast.literal_eval(module_before):
                if ast.literal_eval(module)[key] in ast.literal_eval(module_before).values():
                    return JsonResponse({"code": 50000, "message": "该模块已经存在"})
                else:
                  os.system("cd {} && mkdir {}".format(os.path.join(os.path.join(settings.BASE_DIR, alias), 'testcase'),
                                                     'test_' + key))



        info = list(ProjectInfo.objects.filter(name=name).values("id", "name", "alias", "dec", 'db', 'plat'))

        return JsonResponse({"code": 20000, "data": info, "message": "编辑成功"})
