# Generated by Django 3.1.5 on 2021-01-28 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='标题')),
                ('uil', models.CharField(max_length=68, verbose_name='域名')),
                ('headers', models.CharField(max_length=200, verbose_name='公共请求头')),
                ('payload', models.CharField(max_length=300, verbose_name='公共请求参数')),
                ('plat', models.CharField(max_length=12, verbose_name='平台')),
            ],
        ),
        migrations.CreateModel(
            name='CaseManage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='用例名')),
                ('vars', models.CharField(max_length=128, null=True, verbose_name='形参')),
                ('params', models.CharField(max_length=128, null=True, verbose_name='实参')),
                ('marks', models.CharField(max_length=128, null=True, verbose_name='标识')),
                ('result', models.CharField(default='', max_length=128, null=True, verbose_name='结果')),
                ('report', models.CharField(max_length=256, null=True, verbose_name='报告')),
                ('comment', models.CharField(max_length=568, null=True, verbose_name='描述')),
                ('module', models.CharField(max_length=64, null=True, verbose_name='模块')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('createuser', models.CharField(max_length=128, null=True, verbose_name='创建者')),
            ],
        ),
        migrations.CreateModel(
            name='DbInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='标题')),
                ('ip', models.CharField(max_length=64, verbose_name='数据库ip')),
                ('database', models.CharField(max_length=64, verbose_name='数据库名')),
                ('port', models.CharField(max_length=64, verbose_name='端口')),
                ('username', models.CharField(max_length=64, verbose_name='登录账户')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64, verbose_name='姓名')),
                ('mobile', models.CharField(max_length=128, verbose_name='账户')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('creat_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=128, verbose_name='token')),
                ('creat_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(max_length=32, on_delete=django.db.models.deletion.CASCADE, to='web.userinfo')),
            ],
        ),
        migrations.CreateModel(
            name='StepManage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='方法名')),
                ('returns', models.CharField(max_length=128, null=True, verbose_name='方法名')),
                ('singelapi', models.CharField(max_length=128, null=True, verbose_name='接口方法名')),
                ('params', models.CharField(max_length=128, null=True, verbose_name='实参')),
                ('desc', models.CharField(max_length=568, null=True, verbose_name='描述')),
                ('case', models.ForeignKey(max_length=64, on_delete=django.db.models.deletion.PROTECT, to='web.casemanage')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='项目名')),
                ('alias', models.CharField(max_length=64, verbose_name='别名')),
                ('dec', models.CharField(blank=True, max_length=200, null=True, verbose_name='描述')),
                ('module', models.CharField(max_length=64, null=True, verbose_name='模块')),
                ('creatdate', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('db', models.ForeignKey(max_length=32, on_delete=django.db.models.deletion.PROTECT, to='web.dbinfo')),
                ('plat', models.ForeignKey(max_length=32, on_delete=django.db.models.deletion.PROTECT, to='web.apiinfo')),
            ],
        ),
        migrations.CreateModel(
            name='InfuncManage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='方法名')),
                ('returns', models.CharField(max_length=128, null=True, verbose_name='返回')),
                ('infunc', models.CharField(max_length=128, null=True, verbose_name='内置方法名')),
                ('params', models.CharField(max_length=128, null=True, verbose_name='实参')),
                ('desc', models.CharField(max_length=568, null=True, verbose_name='描述')),
                ('case', models.ForeignKey(max_length=64, on_delete=django.db.models.deletion.PROTECT, to='web.casemanage')),
            ],
        ),
        migrations.AddField(
            model_name='casemanage',
            name='project',
            field=models.ForeignKey(max_length=64, null=True, on_delete=django.db.models.deletion.PROTECT, to='web.projectinfo'),
        ),
        migrations.CreateModel(
            name='AssertManage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='断言名')),
                ('comparatorbef', models.CharField(max_length=128, verbose_name='比较数据')),
                ('comparatorafter', models.CharField(max_length=128, verbose_name='被比较数据')),
                ('type', models.CharField(max_length=128, verbose_name='比较类型')),
                ('desc', models.CharField(max_length=568, null=True, verbose_name='描述')),
                ('case', models.ForeignKey(max_length=64, on_delete=django.db.models.deletion.PROTECT, to='web.casemanage')),
            ],
        ),
        migrations.CreateModel(
            name='ApiManage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('functionName', models.CharField(max_length=64, verbose_name='方法名')),
                ('vars', models.CharField(default='*args,**wkargs', max_length=128, verbose_name='变量')),
                ('paras', models.CharField(max_length=128, null=True, verbose_name='实参')),
                ('url', models.CharField(max_length=64, verbose_name='url')),
                ('plat', models.CharField(max_length=20, verbose_name='平台')),
                ('method', models.CharField(max_length=32, verbose_name='方法')),
                ('headers', models.CharField(default={}, max_length=128, verbose_name='请求头')),
                ('payload', models.CharField(default={}, max_length=128, verbose_name='请求参数')),
                ('comment', models.CharField(max_length=128, null=True, verbose_name='备注')),
                ('result', models.CharField(default='', max_length=128, null=True, verbose_name='结果')),
                ('log', models.CharField(max_length=256, null=True, verbose_name='日志')),
                ('createuser', models.CharField(max_length=128, null=True, verbose_name='创建者')),
                ('creatdate', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('project', models.ForeignKey(max_length=64, on_delete=django.db.models.deletion.PROTECT, to='web.projectinfo')),
            ],
        ),
    ]
