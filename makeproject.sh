#!/bin/bash


#进入venv目录
cd $1
pwd
source bin/activate
#进入项目目录
cd ../
pwd
python manage.py startapp $2

cd $2

mkdir config
mkdir conftest
mkdir testcase
mkdir singelapi
mkdir log
mkdir runresult


cd  config
touch base.ini


