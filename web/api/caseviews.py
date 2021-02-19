import os, sys, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf.settings")
django.setup()
from django.conf import settings

current_path = settings.BASE_DIR
if current_path not in sys.path:
    sys.path.append(current_path)
from django.http import JsonResponse
from rest_framework.views import APIView

from web.models import ProjectInfo, ApiManage, UserInfo,CaseManage,StepManage,InfuncManage,AssertManage

from django.conf import settings
from tools.log_tool import Logger

from tools.configparser_tool import ConfigparserUse
from django.db import transaction
from string import Template
from django.db.models import Q
import ast,inspect

from .infunc import InfuncAll


class CaseManageListView(APIView):

    def get(self, request):
        title = request.GET.get("title")
        project = request.GET.get("project") if request.GET.get("project") !="请选择" else ""
        print(project)
        module = request.GET.get("module") if request.GET.get("module")!="请选择" else ""
        page = int(request.GET.get("page"))
        limit = int(request.GET.get("limit"))
        marks = str(request.GET.get("marks")).split(",") if request.GET.get("marks") else []

        query = CaseManage.objects
        project_info = ProjectInfo.objects.filter(name=project) if project else None
        print(project_info)
        if title:
            query = query.filter(title__contains=title)
            print(query)
        if project :
            query = query.filter(project=project_info[0])
            print(query)
        if module:
            query = query.filter(module=module)
            print(query)
        if marks:
            query = query.filter(marks=marks)
            print(query)
        print(query)
        dataList = list(query.values('id', 'project', 'title', 'module', 'vars', 'marks',
                                      'params', 'comment', 'result', 'report'))
        for i in dataList:
            i['project'] = ProjectInfo.objects.get(id=i['project']).name
        count = len(dataList)
        if page * limit < count:
            dataList = list(dataList)[(page - 1) * limit:page * limit]
        else:
            dataList = list(dataList)[(page - 1) * limit:count]
        return JsonResponse({'code': 20000, 'message': "success", 'data': {"items": dataList, 'total': count}})


class AddCaseView(APIView):
    def post(self,request):
        title = str(request.data.get('title'))
        project = str(request.data.get('project'))
        module = str(request.data.get('module'))
        marks = ast.literal_eval(request.data.get('marks') if request.data.get('marks') else '[]')
        vars = ast.literal_eval(request.data.get('vars') if request.data.get('vars') else '[]')
        params = ast.literal_eval(request.data.get('params') if request.data.get('params') else '[]')
        comment = str(request.data.get('comment')) if request.data.get('comment') else ""
        caseinfo = CaseManage.objects.filter(title=title)
        project_info = ProjectInfo.objects.filter(name=project)[0]
        if not (isinstance(marks,list) or isinstance(vars,list) or isinstance(params,list)):
            return JsonResponse({"code": 50000, "message": "marks、形参、实参 要是list的格式"})
        if caseinfo.exists():
            return JsonResponse({"code":50000,"message":"已经存在该用例"})
        if not isinstance(marks,list) or not isinstance(vars,list) or not isinstance(params,list):
            return JsonResponse({"code": 50000, "message": "marks或者形参、实参输入格式不对"})
        if not title.startswith("test_"):
            title= "test_"+title

        try:
           with transaction.atomic():
            CaseManage.objects.create(title=title,project=project_info,module=module,marks=marks,vars=vars,params=params,comment=comment)
        except Exception as e:

            Logger(os.path.join(settings.BASE_DIR,'log')).rotateInputLog().error(e)
            return JsonResponse({"code": 50000, "message": "创建失败"})
        dataList = list(CaseManage.objects.filter(title=title).values('id', 'project', 'title', 'module', 'vars', 'marks',
                                      'params', 'comment', 'result', 'report'))
        return JsonResponse({"code": 20000, "data": dataList, "message": "添加成功"})

class GetStepView(APIView):
    def get(self,request):
        caseid = request.GET.get("0")

        caseinfo = CaseManage.objects.get(id=caseid)

        stepinfo=StepManage.objects.filter(case=caseinfo).values('order','singelapi',"params","desc")

        infuncinfo = InfuncManage.objects.filter(case=caseinfo).values('order','infunc',"params","desc")
        print(list(infuncinfo))
        steplist =[]
        steplist.extend(list(stepinfo))
        steplist.extend(list(infuncinfo))
        print(steplist)

        steplist.sort(key=lambda i:int(i['order']))

        modify_steplist = []
        print(steplist)
        for i in steplist:
              i[": "]=i["order"]
              if "singelapi" in i.keys():
                  i[" 接口方法名 : "] = i["singelapi"]
                  del i["singelapi"]
              if "infunc" in i.keys():
                i[" 内置方法名 : "] = i["infunc"]
                del i["infunc"]
              i[" 参数 : "] = i["params"]
              i[" 描述 : "] = i["desc"]

              del i["order"]
              del i["params"]
              del i["desc"]
              list_f = []
              for key,value in i.items():
                list_f.append(key+value)
              str_f ="  ---  ".join(list_f)
              modify_steplist.append(str_f)
        print(modify_steplist)

        return JsonResponse({"code":20000,'data': modify_steplist})


class AddCaseStepView(APIView):

    def post(self,request):
        order = request.data.get("order")
        if not order.isdigit():
            return JsonResponse({"code": 50000, "message": "序号要求输入纯数字"})

        singelapi = str(request.data.get('singleapi'))
        params = ast.literal_eval(request.data.get('params')if request.data.get('params') else '[]')
        returns = str(request.data.get('returns'))
        desc = str(request.data.get('desc'))
        case_id = str(request.data.get('caseid'))
        case_info = CaseManage.objects.filter(id = case_id)[0]
        print(case_info)
        if StepManage.objects.filter(case=case_info,order=order).exists() and InfuncManage.objects.filter(case=case_info,order=order).exists():
            return JsonResponse({"code": 50000, "message": "步骤序号重复"})
        try:
            with transaction.atomic():
                StepManage.objects.create(order=order,singelapi=singelapi,params=params,returns=returns,desc=desc,case=case_info)
        except Exception as e:
           print(e)
           Logger(os.path.join(settings.BASE_DIR, 'log')).rotateInputLog().error(e)
           return JsonResponse({"code": 50000, "message": "创建失败"})
        dataList = list(StepManage.objects.filter(case=case_info,order=order).values('order', 'singelapi'))
        return JsonResponse({"code": 20000, "data": dataList, "message": "添加成功"})

class AddCaseInfuncView(APIView):

    def post(self,request):
        order = request.data.get("order")
        if not order.isdigit():
            return JsonResponse({"code": 50000, "message": "序号要求输入纯数字"})

        infuncname = str(request.data.get('singleapi'))
        params = ast.literal_eval(request.data.get('params')if request.data.get('params') else '[]')
        returns = str(request.data.get('returns'))
        desc = str(request.data.get('desc'))
        case_id = str(request.data.get('caseid'))
        case_info = CaseManage.objects.filter(id = case_id)[0]
        print(case_info)
        if StepManage.objects.filter(case=case_info,order=order).exists() and InfuncManage.objects.filter(case=case_info,order=order).exists():
            return JsonResponse({"code": 50000, "message": "步骤序号重复"})
        try:
            with transaction.atomic():
                InfuncManage.objects.create(order=order,infunc=infuncname,params=params,returns=returns,desc=desc,case=case_info)
        except Exception as e:
           print(e)
           Logger(os.path.join(settings.BASE_DIR, 'log')).rotateInputLog().error(e)
           return JsonResponse({"code": 50000, "message": "创建失败"})
        dataList = list(InfuncManage.objects.filter(case=case_info,order=order).values('order', 'infunc'))
        return JsonResponse({"code": 20000, "data": dataList, "message": "添加成功"})
class AddCaseAssertView(APIView):

    def post(self,request):
        order = request.data.get("order")
        if not order.isdigit():
            return JsonResponse({"code": 50000, "message": "序号要求输入纯数字"})
        type = str(request.data.get('type'))
        num = str(request.data.get('num')) if request.data.get('num') else ""
        comparatorbef = str(request.data.get('comparatorbef'))
        comparatorafter = str(request.data.get('comparatorafter'))
        desc = str(request.data.get('desc'))
        case_id = str(request.data.get('caseid'))
        case_info = CaseManage.objects.filter(id = case_id)[0]
        print(case_info)
        if not num.isdigit() and num:
            return JsonResponse({"code": 50000, "message": "num 请输入数字"})
        if AssertManage.objects.filter(case=case_info,order=order).exists():
            return JsonResponse({"code": 50000, "message": "步骤序号重复"})
        try:
            with transaction.atomic():
                case_info.np = 1
                case_info.save()
                AssertManage.objects.create(order=order,type=type,fornum=num,comparatorbef=comparatorbef,comparatorafter=comparatorafter,desc=desc,case=case_info)

                dataList = list(AssertManage.objects.filter(case=case_info, order=order).values('order', 'type'))
        except Exception as e:
           print(e)
           Logger(os.path.join(settings.BASE_DIR, 'log')).rotateInputLog().error(e)
           return JsonResponse({"code": 50000, "message": "创建失败"})

        return JsonResponse({"code": 20000, "data": dataList, "message": "添加成功"})

class GetInfuncList(APIView):
    def get(self,request):

       infun_list = [i for i in dir(InfuncAll) if callable(getattr(InfuncAll, i)) and not inspect.isbuiltin(getattr(InfuncAll, i))]
       print(infun_list[19:])
       return JsonResponse({"code": 20000, "data": infun_list, "message": "添加成功"})


class DeleteCaseView(APIView):
    def post(self, request):
        for i in request.data:
           info = CaseManage.objects.get(id=i.get('id',''))
           step_info =StepManage.objects.filter(case=info)
           infun_info = InfuncManage.objects.filter(case=info)
           assert_info = AssertManage.objects.filter(case=info)
           for j in step_info:
                j.delete()
           for j in infun_info:
                j.delete()
           for j in assert_info:
                j.delete()
           info.delete()
        return JsonResponse({"code": 20000, "message": "删除成功"})


class UpdateCaseView(APIView):
    def post(self,request):
        print(request.data)
        id = int(request.data.get("id"))
        title = str(request.data.get("title"))
        marks = ast.literal_eval(request.data.get("marks")) if request.data.get("marks") else '[]'
        vars = ast.literal_eval(request.data.get("vars")) if request.data.get("vars") else '[]'
        params = ast.literal_eval(request.data.get("params")) if request.data.get("params") else '[]'
        case_info = CaseManage.objects.get(id=id)
        if CaseManage.objects.get(title=title) and title!=case_info.title:
            return JsonResponse({"code": 50000, "message": "已经存在同名用例了"})
        if not (isinstance(marks,list) or isinstance(vars,list) or isinstance(params,list)):
            return JsonResponse({"code": 50000, "message": "marks、形参、实参 要是list的格式"})
        if case_info:
            try:
              with transaction.atomic():
                  case_info.title= request.data.get("title")
                  case_info.marks = marks
                  case_info.vars = vars
                  case_info.params = params
                  case_info.comment = request.data.get("comment") if request.data.get("comment") else ""
                  case_info.np = 2
                  case_info.save()

            except Exception as e:
                print(e)
                Logger(os.path.join(settings.BASE_DIR, 'log')).rotateInputLog().error(e)
                return JsonResponse({"code": 50000, "message": "更新失败"})
        return JsonResponse({"code": 20000, "message": "更新成功"})


class RunCaseView(APIView):
    def post(self,request):

        for i in request.data:
            print(i)
        return JsonResponse({"code": 20000, "message": "更新成功"})


class Jm(APIView):
    def get(self,request):
        import time,random
        t = random.randrange(1,13)
        print(t)
        time.sleep(t)
        return JsonResponse({"CODE":"200"})




