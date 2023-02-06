import os
import time
import re
import django
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from requests import request
from lib.action import Action
from blog import models
import json
from django.contrib import messages

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webshell.settings")  # project_name指项目名
django.setup()
to_action = Action()


def drvice_true(request):
    context = {"data": []}
    data = {}
    for i in models.Drvice.objects.all():
        if i.drvice_type not in data:
            data['{}'.format(i.drvice_type)] = []
            data['{}'.format(i.drvice_type)].append({"name": "{}".format(i.drvice_name), "id": i.id})
            continue
        if i.drvice_type in data:
            data['{}'.format(i.drvice_type)].append({"name": "{}".format(i.drvice_name), "id": i.id})
    children = []
    for i in data:
        a = {'name': i, 'children': data['{}'.format(i)]}
        children.append(a)
    context['data'].append({"name": "drvice", "children": children})
    # print(json.dumps(context))
    return JsonResponse(data=context)


def srcipt_true(request):
    context = {"data": []}
    data1 = {}
    for i in models.Script.objects.all():
        if i.drvice_type not in data1:
            data1['{}'.format(i.drvice_type)] = []
            data1['{}'.format(i.drvice_type)].append({"name": "{}".format(i.script_name), "id": i.id})
            continue
        if i.drvice_type in data1:
            data1['{}'.format(i.drvice_type)].append({"name": "{}".format(i.script_name), "id": i.id})
    children = []
    for i in data1:
        a = {'name': i, 'children': data1['{}'.format(i)]}
        children.append(a)
    context['data'].append({"name": "srcipt", "children": children})
    # print(json.dumps(context))
    return JsonResponse(data=context)


def index(request):
    context = {}
    # print(request.method)
    # if request.method == 'POST':
    #     # 1.3 获取post除文件外所有数据 -->dict
    #     print(request.POST)
    #     # 1.4 获取
    #     print(request.POST.getlist('ip'))
    context['hello'] = 'Hello World!'
    # context['drvice'] = DrviceOrm.all()
    # context['script'] = ScriptOrm.all()
    # data = {}
    # for i in models.Drvice.objects.all():
    #     if i.drvice_type not in data:
    #         data['{}'.format(i.drvice_type)] = []
    #         data['{}'.format(i.drvice_type)].append([i.id, i.drvice_name])
    #         continue
    #     if i.drvice_type in data:
    #         data['{}'.format(i.drvice_type)].append([i.id, i.drvice_name])
    # data1 = {}
    # for i in models.Script.objects.all():
    #     if i.drvice_type not in data1:
    #         data1['{}'.format(i.drvice_type)] = []
    #         data1['{}'.format(i.drvice_type)].append([i.id, i.script_name])
    #         continue
    #     if i.drvice_type in data1:
    #         data1['{}'.format(i.drvice_type)].append([i.id, i.script_name])
    # context['drvice'] = data
    # print(data)
    # print(data1)
    # context['script'] = data1
    return render(request, 'index.html', context)


def test(request):
    context = {}
    print(request.method)
    if request.method == 'POST':
        # 1.3 获取post除文件外所有数据 -->dict
        print(request.POST)
        # 1.4 获取
        print(request.POST.getlist('ip'))
    context['hello'] = "'Hello World!'"
    # context['script'] = ScriptOrm.all()
    list1 = [{'id': 1, 'type': 2, 'c': 3}, {'id': 11, 'type': 12, 'c': 31}]
    context['drvice_num'] = len(list1)
    context['drvice'] = json.dumps(list1, indent=2)
    context['script'] = [{'id': 10, 'type': 20, 'res': 30}, {'id': 11, 'type': 12, 'res': 31}]
    return JsonResponse(data=context)


input_data = {}


def create_input(request):
    data = json.loads(request.body.decode())
    pattern = re.compile(r'<(.*?)>')
    a = {}
    b = []
    for i in data['srciptid']:
        # print(i)
        reson = models.Script.objects.get(id=i).script_reson
        match = pattern.findall(reson)
        if match:
            for i in match:
                a['{}'.format(i)] = ''
                b.append(i)
    context = {"data": a, "data1": b}
    to_action.input_data = a
    # print(a)
    return JsonResponse(context)


def to_reson(request):
    # print(request.method)
    data = json.loads(request.body.decode())
    input_data = to_action.input_data
    print(data)
    if input_data != {}:
        for d in input_data:
            input_data['{}'.format(d)] = data['{}'.format(d)]
    # print(input_data)
    context = {'ret_data2': ['conf t']}
    # print(data['srcipt']['name'])
    for i in data['srciptid']:
        # print(i)
        a = models.Script.objects.get(id=i).script_reson
        for b in input_data:
            if '<{}>'.format(b) in a:
                a = a.replace('<{}>'.format(b), '{}'.format(input_data['{}'.format(b)]))
        context['ret_data2'].append(a)
        # context['ret_data2'] = context['ret_data2'] + models.Script.objects.get(
        #     script_name='{}'.format(i))
    # print(context['ret_data2'])
    to_action.limit_data = context['ret_data2']
    messages.success(request, '成功生成')
    return JsonResponse(data=context)


def clean_all(request):
    to_action.clean_data()
    context = {"status": 200}

    return JsonResponse(data=context)


# def update_reson(request):
#     data = json.loads(request.body.decode())
#     to_action.limit_data = data['srcipt']
#     context = {"status": 200}
#     return JsonResponse(data=context)


def to_data(request):
    context = {}
    # data = request.POST.get('data')
    data = json.loads(request.body.decode())
    # ip = data['ip']
    # network = data['network']
    data1 = data['drviceid']
    # data2 = data['srcipt']
    # reson = ['conf t']
    passwd = []
    login = []
    user = []
    port = []
    # for i in data2:
    #     reson.append(
    #         models.Script.objects.get(script_name='{}'.format(i)).script_reson.replace('<ip>', ip).replace('<network>',
    #                                                                                                        network))
    reson = to_action.limit_data
    for i in data1:
        a = models.Drvice.objects.get(id=i)
        login.append(a.drvice_host)
        user.append(a.drvice_user)
        port.append(a.drvice_port)
        if int(models.Setting.objects.get(setting_name='is_key').setting_value) == 0:
            passwd.append(a.drvice_passwd)
    # print(reson)
    # print(login)
    # print(user)
    # print(port)
    # print(passwd)
    ret_data = to_action.action_ssh(login=login, user=user, passwd=passwd,
                                    port=port, script_reson=reson)
    # print('给前端', ret_data)
    context['ret_data1'] = ret_data
    return JsonResponse(data=context)
