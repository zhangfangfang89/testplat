"""drf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from web.api.apiviews import *
from web.api.singelapiviews import *
from web.api.caseviews import *
from web.api.dbviews import DbListView, AddDbView, DeleteDbView, UpdateDbView, DbListViewAll
from web.api.projectviews import *
from web.api.userviews import LoginView, UserInfoView, LogoutView, UsermanageView, DeleteUserView

urlpatterns = [
    path('user/login', LoginView.as_view()),
    path('user/info', UserInfoView.as_view()),
    path('user/logout', LogoutView.as_view()),
    path('user/list', UsermanageView.as_view()),
    path('user/create', UsermanageView.as_view()),
    path('user/delete', DeleteUserView.as_view()),
    # **********************project***********
    path('project/list', ProjectListView.as_view()),
    path('project/create', AddProjectView.as_view()),
    path('project/delete', DeleteProjectView.as_view()),
    path('project/update', UpdateProjectView.as_view()),
    path('project/all/list', ProjectListViewAll.as_view()),
    path('module/list',ModuleListView.as_view()),
    # **********************db***********
    path('db/list', DbListView.as_view()),
    path('db/create', AddDbView.as_view()),
    path('db/delete', DeleteDbView.as_view()),
    path('db/update', UpdateDbView.as_view()),
    path('db/list/all', DbListViewAll.as_view()),
    # **********************接口信息配置***********
    path('api/list', ApiListView.as_view()),
    path('api/create', AddApiView.as_view()),
    path('api/delete', DeleteApiView.as_view()),
    path('api/update', UpdateApiView.as_view()),
    path('api/list/all', ApiListViewAll.as_view()),
    # **********************接口管理配置***********
    path('testapi/list', ApiManageListView.as_view()),
    path('testapi/create', AddApiManageView.as_view()),
    path('testapi/delete', DeleteApiManageView.as_view()),
    path('testapi/update', UpdateApiManageView.as_view()),
    path('testapi/list/all', ApiManageListViewAll.as_view()),
    path('testapi/run', RunApiManageView.as_view()),
    # *********************case用例管理*********
    path('testcase/list', CaseManageListView.as_view()),
    path('testcase/create', AddCaseView.as_view()),
    path('testcasestep/create', AddCaseStepView.as_view()),
    path('testcaseinfunc/create', AddCaseInfuncView.as_view()),
    path('testcaseassert/create', AddCaseAssertView.as_view()),
    path('testcase/step/list', GetStepView.as_view()),
    path('testcase/delete', DeleteCaseView.as_view()),
    path('testcase/update', UpdateCaseView.as_view()),
    path('testcase/list/all', ApiManageListViewAll.as_view()),
    path('testcase/run', RunCaseView.as_view()),
    #*****************内置函数的***********
    path("testcase/infunc/list/",GetInfuncList.as_view()),


    path("jmeter/",Jm.as_view()),
]
