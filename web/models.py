from django.db import models


# Create your models here.
# 用户的model
class UserInfo(models.Model):
    username = models.CharField("姓名", max_length=64)
    mobile = models.CharField("账户", max_length=128)
    password = models.CharField("密码", max_length=32)
    creat_date = models.DateTimeField("创建时间", auto_now_add=True)


class UserToken(models.Model):
    user = models.ForeignKey(to='UserInfo', max_length=32, on_delete=models.CASCADE)
    token = models.CharField("token", max_length=128)
    creat_date = models.DateTimeField("创建时间", auto_now_add=True)


# 项目的model

class ProjectInfo(models.Model):
    name = models.CharField("项目名", max_length=64)
    alias = models.CharField("别名", max_length=64)
    dec = models.CharField("描述", max_length=200, blank=True, null=True)
    db = models.ForeignKey(to='DbInfo', max_length=32, on_delete=models.PROTECT)
    plat = models.ForeignKey(to='ApiInfo', max_length=32, on_delete=models.PROTECT)
    module = models.CharField("模块", max_length=64, null=True)
    creatdate = models.DateTimeField("创建时间", auto_now_add=True)


class DbInfo(models.Model):
    name = models.CharField("标题", max_length=64)
    ip = models.CharField("数据库ip", max_length=64)
    database = models.CharField("数据库名", max_length=64)
    port = models.CharField("端口", max_length=64)
    username = models.CharField("登录账户", max_length=64)
    password = models.CharField("密码", max_length=64)


class ApiInfo(models.Model):
    name = models.CharField("标题", max_length=64)
    uil = models.CharField("域名", max_length=68)
    headers = models.CharField("公共请求头", max_length=200)
    payload = models.CharField("公共请求参数", max_length=300)
    plat = models.CharField("平台", max_length=12)


# 接口model


class ApiManage(models.Model):
    functionName = models.CharField('方法名', max_length=64)
    vars = models.CharField('变量', max_length=128, default="*args,**wkargs")
    paras = models.CharField('实参', max_length=128, null=True)
    url = models.CharField('url', max_length=64)
    plat = models.CharField('平台', max_length=20)
    method = models.CharField('方法', max_length=32)
    headers = models.CharField('请求头', max_length=128, default={})
    payload = models.CharField('请求参数', max_length=128, default={})
    comment = models.CharField('备注', max_length=128, null=True)
    result = models.CharField('结果', max_length=128, default='', null=True)
    log = models.CharField('日志', max_length=1280,null=True)
    project = models.ForeignKey(to='ProjectInfo', max_length=64, on_delete=models.PROTECT)
    createuser = models.CharField('创建者', max_length=128, null=True)
    creatdate = models.DateTimeField("创建时间", auto_now_add=True)

#case model

class CaseManage(models.Model):
    title = models.CharField('用例名', max_length=128)
    vars = models.CharField('形参', max_length=128,null=True)
    params = models.CharField('实参', max_length=128,null=True)
    marks = models.CharField('标识', max_length=128,null=True)
    result =models.CharField('结果', max_length=128, default='', null=True)
    report=models.CharField('报告', max_length=256,null=True)
    comment = models.CharField('描述', max_length=568,null=True)
    project = models.ForeignKey(to='ProjectInfo', max_length=64, on_delete=models.PROTECT,null=True)
    module = models.CharField("模块", max_length=64, null=True)
    np = models.CharField("是新增还是更新", max_length=64, null=True)
    create_date = models.DateTimeField("创建时间", auto_now_add=True)
    createuser = models.CharField('创建者', max_length=128, null=True)

class StepManage(models.Model):
    returns = models.CharField('方法名', max_length=128,null=True)
    singelapi = models.CharField('接口方法名', max_length=128,null=True)
    params =models.CharField('实参', max_length=128,null=True)
    desc = models.CharField('描述', max_length=568,null=True)
    order = models.CharField("序号", max_length=32,null=True)
    case = models.ForeignKey(to='CaseManage', max_length=64, on_delete=models.PROTECT)


class InfuncManage(models.Model):
    returns = models.CharField('返回', max_length=128, null=True)
    infunc = models.CharField('内置方法名', max_length=128, null=True)
    params = models.CharField('实参', max_length=128, null=True)
    desc = models.CharField('描述', max_length=568,null=True)
    order = models.CharField("序号", max_length=32,null=True)
    case = models.ForeignKey(to='CaseManage', max_length=64, on_delete=models.PROTECT)

class AssertManage(models.Model):
    comparatorbef =models.CharField('比较数据', max_length=128)
    comparatorafter =models.CharField('被比较数据', max_length=128)
    type=models.CharField('比较类型', max_length=128)
    case = models.ForeignKey(to='CaseManage', max_length=64, on_delete=models.PROTECT)
    fornum = models.CharField('循环次数', max_length=128,null=True)
    order = models.CharField("序号", max_length=32,null=True)
    desc = models.CharField('描述', max_length=568,null=True)
