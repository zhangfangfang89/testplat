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

from web.models import ProjectInfo, ApiManage, UserInfo

from django.conf import settings
from tools.log_tool import Logger

from tools.configparser_tool import ConfigparserUse
from django.db import transaction
from string import Template
from django.db.models import Q
import ast


# 生成项目和配置文件

def getCode():
    str = \
        """
    def ${function_name}(self,$vars*args,**wkargs):
        " '''$comment''' "
        log= theLog('$project')
        self.set_url('$dir_base','$url',platForm='$form')
        self.set_payload('$dir_base',$data,platForm='$form')
        self.set_headers('$dir_base',$headers,platForm='$form')
        self.headers.update({ "Cookie":self.cookies})
        try:
            self.$method()
            if self.code == 200:
                log.rotateInputLog().info("${comment}接口成功"+json.dumps(self.resp_json))
                return self.resp_json
            else:
                log.rotateInputLog().error("${comment}接口失败，非200！" + json.dumps(self.resp_json))
                raise Exception("${comment}接口失败，非200！")
        except Exception as e:
            log.rotateInputLog().error(e)

        $d
        $d

    """
    return str


class ApiManageListViewAll(APIView):

    def get(self, request):
        project = request.GET.get('0')
        print(project)
        project_info = ProjectInfo.objects.filter(name=project)[0]
        query = ApiManage.objects.filter(project=project_info,result='pass')
        print(query)

        dataList = query.values("functionName")


        return JsonResponse({'code': 20000, 'message': "success", 'data': {"items": list(dataList)}})


class ApiManageListView(APIView):
    """查询数据"""

    def get(self, request):
        name = request.GET.get("functionName")
        project = request.GET.get("project")
        page = int(request.GET.get("page"))
        limit = int(request.GET.get("limit"))
        query = ApiManage.objects
        project_info = ProjectInfo.objects.filter(name=project)

        if project :
            query = query.filter(project=project_info[0])
        if  name:
            query = query.filter(functionName__contains=name)
        dataList = list(query.values('id', 'project', 'functionName', 'method', 'url', 'headers',
                                     'payload', 'vars', 'paras', 'plat', 'comment', 'result', 'log'))
        for i in dataList:
            i['project'] = ProjectInfo.objects.get(id=i['project']).name
        count = len(dataList)
        if page * limit < count:
            dataList = list(dataList)[(page - 1) * limit:page * limit]
        else:
            dataList = list(dataList)[(page - 1) * limit:count]
        return JsonResponse({'code': 20000, 'message': "success", 'data': {"items": dataList, 'total': count}})


class AddApiManageView(APIView):

    def post(self, request):

        token = request.META['HTTP_X_TOKEN']
        mobile = token.split('.')[0]
        name = request.data.get('functionName')
        project = request.data.get("project")
        method = request.data.get('method')
        url = request.data.get('url')
        headers = request.data.get('headers')
        headers = '{}' if not headers else headers
        payload = request.data.get('payload')
        payload = '{}' if not payload else payload

        vars = request.data.get("vars")
        vars = "[]" if not vars else vars
        paras = request.data.get('paras')
        paras = "[]" if not paras else paras
        comment = request.data.get('comment')
        plat = request.data.get("plat")
        alias = ProjectInfo.objects.get(name=project).alias
        info = ApiManage.objects.filter(functionName=name)
        dir_base = os.path.join(os.path.join(os.path.join(settings.BASE_DIR, alias), 'config'), 'base.ini')
        if info.exists():
            return JsonResponse({"code": 50000, "message": "接口方法名不能重复"})

        if not isinstance(ast.literal_eval(headers), dict) or not isinstance(ast.literal_eval(payload), dict):
            return JsonResponse({"code": 50000, "message": "请求头或者请求参数输入格式不对"})
        else:
            headers = ast.literal_eval(headers)
            payload = ast.literal_eval(payload)

        if not isinstance(ast.literal_eval(vars), list):
            return JsonResponse({"code": 50000, "message": "形参输入格式不对，请求输入list类型"})

        if not isinstance(ast.literal_eval(paras), list):
            return JsonResponse({"code": 50000, "message": "形参输入格式不对，请求输入list类型"})

        try:
            with transaction.atomic():
                project_info = ProjectInfo.objects.filter(name=project)
                ApiManage.objects.create(project=project_info[0], functionName=name, method=method, url=url,
                                         headers=headers, payload=payload, vars=vars, paras=paras, comment=comment,
                                         createuser=mobile, plat=plat)

                dataList = list(
                    ApiManage.objects.filter(functionName=name).values('project', 'functionName', 'method', 'url',
                                                                       'headers',
                                                                       'payload', 'vars', 'comment', 'result', 'log'))

                vars = ast.literal_eval(vars)
                if vars == []:
                    vars = ''.join(vars)
                else:
                    vars = ''.join(vars) + ','

                if vars == []:
                    paras = ""
                else:
                    paras = ast.literal_eval(paras)
                    paras = ''.join(paras)
                # 接下来要生成脚本
                print(getCode())
                temp = Template(getCode())
                if not comment:
                    comment = ""
                functionName = temp.substitute(dir_base=dir_base, project=alias, function_name=name, url=url,
                                               data=payload,
                                               headers=headers,
                                               method=method, d='\r', vars=vars, comment=comment, form=plat)

                with open("{}/{}/singelapi/allapi.py".format(settings.BASE_DIR, alias), 'a+') as f:
                    f.writelines(functionName)

        except Exception as e:
            print(e)
            return JsonResponse({"code": 50000, "message": "创建失败"})

        return JsonResponse({"code": 20000, "data": dataList, "message": "添加成功"})


class DeleteApiManageView(APIView):
    def post(self, request):
        info = ApiManage.objects.get(id=request.data.get('id'))
        info.delete()

        return JsonResponse({"code": 20000, "message": "删除成功"})


class UpdateApiManageView(APIView):
    def post(self, request):
        token = request.META['HTTP_X_TOKEN']
        mobile = token.split('.')[0]
        name = request.data.get('functionName')
        project = request.data.get("project")
        method = request.data.get('method')
        url = request.data.get('url')
        headers = request.data.get('headers')
        headers = '{}' if not headers else headers
        payload = request.data.get('payload')
        payload = '{}' if not payload else payload
        vars = request.data.get("vars")
        vars = "[]" if not vars else vars
        paras = request.data.get('paras')
        paras = "[]" if not paras else paras
        comment = request.data.get('comment')
        plat = request.data.get("plat")
        alias = ProjectInfo.objects.get(name=project).alias
        dir_base = os.path.join(os.path.join(os.path.join(settings.BASE_DIR, alias), 'config'), 'base.ini')
        if not isinstance(ast.literal_eval(headers), dict) or not isinstance(ast.literal_eval(payload), dict):
            return JsonResponse({"code": 50000, "message": "请求头或者请求参数输入格式不对"})
        else:
            headers = ast.literal_eval(headers)
            payload = ast.literal_eval(payload)

        if not isinstance(ast.literal_eval(vars), list):
            return JsonResponse({"code": 50000, "message": "形参输入格式不对，请求输入list类型"})
        if not isinstance(ast.literal_eval(paras), list):
            return JsonResponse({"code": 50000, "message": "形参输入格式不对，请求输入list类型"})

        try:
            with transaction.atomic():
                project_info = ProjectInfo.objects.filter(name=project)
                ApiManage.objects.filter(functionName=name).update(project=project_info[0], method=method, url=url,
                                                                   headers=headers, payload=payload, vars=vars,
                                                                   comment=comment,
                                                                   createuser=mobile, plat=plat)

                dataList = list(
                    ApiManage.objects.filter(functionName=name).values('project', 'functionName', 'method', 'url',
                                                                       'headers',
                                                                       'payload', 'vars', 'paras', 'plat', 'comment',
                                                                       'result',
                                                                       'log'))
                vars = ast.literal_eval(vars)
                if vars == []:
                    vars = ''.join(vars)
                else:
                    vars = ''.join(vars) + ','

                # 接下来要生成脚本
                begin_num = 0
                with open("{}/{}/singelapi/allapi.py".format(settings.BASE_DIR, alias), 'r') as f:
                    all_list = f.readlines()
                for i in range(len(all_list)):
                    if name in all_list[i]:
                        begin_num = i
                print(begin_num)
                os.system("cd {} && chmod +x setting.sh".format(settings.BASE_DIR))
                os.system("cd {} && ./setting.sh {} {} {}".format(settings.BASE_DIR, begin_num-2, begin_num + 18,
                                                                  "{}/{}/singelapi/allapi.py".format(
                                                                      settings.BASE_DIR, alias)))
                temp = Template(getCode())
                if not comment:
                    comment = ""
                functionName = temp.substitute(dir_base=dir_base, project=alias, function_name=name, url=url,
                                               data=payload,
                                               headers=headers,
                                               method=method, d='\r', vars=vars, comment=comment, form=plat)

                with open("{}/{}/singelapi/allapi.py".format(settings.BASE_DIR, alias), 'a+') as f:
                    f.writelines(functionName)

        except Exception as e:
            print(e)
            return JsonResponse({"code": 50000, "message": "编辑失败"})

        return JsonResponse({"code": 20000, "data": dataList, "message": "编辑成功"})


class RunApiManageView(APIView):
    def post(self, request):
        functionName = request.data.get("functionName")
        project = request.data.get("project")
        vars = request.data.get("vars")
        paras = request.data.get('paras')
        alias = ProjectInfo.objects.get(name=project).alias
        # dir_base = os.path.join(os.path.join(os.path.join(settings.BASE_DIR, alias), 'config'), 'base.ini')

        if vars != [] and paras == []:
            return JsonResponse({"code": 50000, "message": "要求输入实参，请进行编辑输入"})
        try:
            paras = ast.literal_eval(paras)
            paras = ''.join(paras)
            begin_num = 0
            with open("{}/{}/singelapi/runapi.py".format(settings.BASE_DIR, alias), 'r') as f:
                all_list = f.readlines()

            for i in range(len(all_list)):
                if "singelapi.allapi import TestApi" in all_list[i]:
                    begin_num = i

            if begin_num != 0:
                print(begin_num)
                dir_runapi = "{}".format(os.path.join(os.path.join(os.path.join(settings.BASE_DIR, alias),'singelapi'),'runapi.py'))
                print(dir_runapi)
                os.system("cd {} && chmod +x setting.sh".format(settings.BASE_DIR))
                os.system("cd {} && ./setting.sh {} {} {}".format(settings.BASE_DIR,begin_num + 1, begin_num + 7,dir_runapi))
            # 还差调用函数
            temp = Template("""
from $alias.singelapi.allapi import TestApi

if __name__ == '__main__':

    tester = TestApi()
    tester.$fun($params)
                   """)

            funccode = temp.substitute(alias=alias, fun=functionName, params=paras)
            res = ''
            print(funccode)
            with open("{}/{}/singelapi/runapi.py".format(settings.BASE_DIR, alias), 'a+') as f:
                f.writelines(funccode)

            result = os.system(
                "python {0}/{1}/singelapi/runapi.py >>{0}/{1}/singelapi/run.txt".format(settings.BASE_DIR, alias))
            if result == 0:
                with open("{}/{}/singelapi/run.txt".format(settings.BASE_DIR, alias), 'r') as f:
                    txt = f.readlines()
                    dir = txt[-1].split('.')[0] + '.log'
                with open(dir, 'r') as f:
                    context = f.readlines()
                    print(context[-1])
                    dir = dir + "-----详细内容：" + context[-1]
                    if "接口成功" in context[-1]:
                        res = 'pass'
                    else:
                        res = 'fail'
            ApiManage.objects.filter(functionName=functionName).update(result=res, log=dir)
            dataList = list(
                ApiManage.objects.filter(functionName=functionName).values('project', 'functionName', 'method', 'url',
                                                                           'headers', 'payload', 'plat', 'vars',
                                                                           'paras',
                                                                           'comment', 'result', 'log'))
        except Exception as e:
            print(e)
            return JsonResponse({"code": 50000, "message": "出错拉~~，请联系开发"})

        return JsonResponse({"code": 20000, "data": dataList})
