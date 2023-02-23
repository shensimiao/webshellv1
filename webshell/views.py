import os
import time
import openai
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


def device_true(request):
    context = {"data": []}
    data = {}
    for i in models.Device.objects.all():
        if i.device_type not in data:
            data['{}'.format(i.device_type)] = []
            data['{}'.format(i.device_type)].append({"name": "{}".format(i.device_name), "id": i.id})
            continue
        if i.device_type in data:
            data['{}'.format(i.device_type)].append({"name": "{}".format(i.device_name), "id": i.id})
    children = []
    a1 = 100000
    for i in data:
        a = {'name': i, 'children': data['{}'.format(i)], 'id': a1}
        a1 = a1 + 1
        children.append(a)
    to_action.device_true = children
    context['data'].append({"name": "device", "children": children})
    # print(json.dumps(context))
    return JsonResponse(data=context)


def srcipt_true(request):
    context = {"data": []}
    data1 = {}
    for i in models.Script.objects.all():
        if i.device_type not in data1:
            data1['{}'.format(i.device_type)] = []
            data1['{}'.format(i.device_type)].append({"name": "{}".format(i.script_name), "id": i.id})
            continue
        if i.device_type in data1:
            data1['{}'.format(i.device_type)].append({"name": "{}".format(i.script_name), "id": i.id})
    children = []
    for i in data1:
        a = {'name': i, 'children': data1['{}'.format(i)]}
        children.append(a)
    to_action.srcipt_true = data1
    context['data'].append({"name": "srcipt", "children": children})
    # print(json.dumps(context))
    return JsonResponse(data=context)


def s_ture(request):
    ids = json.loads(request.body.decode())
    true = to_action.srcipt_true
    print(ids)
    context = {'data': []}
    if ids['device_type']:
        for i in true:
            if ids['device_type'].capitalize() == i.capitalize():
                context['data'].append({"name": "srcipt", "children": [{'name': i, 'children': true['{}'.format(i)]}]})
    print(context)
    return JsonResponse(data=context)


def index(request):
    context = {'hello': 'Hello World!'}
    # print(request.method)
    # if request.method == 'POST':
    #     # 1.3 获取post除文件外所有数据 -->dict
    #     print(request.POST)
    #     # 1.4 获取
    #     print(request.POST.getlist('ip'))
    # context['device'] = deviceOrm.all()
    # context['script'] = ScriptOrm.all()
    # data = {}
    # for i in models.device.objects.all():
    #     if i.device_type not in data:
    #         data['{}'.format(i.device_type)] = []
    #         data['{}'.format(i.device_type)].append([i.id, i.device_name])
    #         continue
    #     if i.device_type in data:
    #         data['{}'.format(i.device_type)].append([i.id, i.device_name])
    # data1 = {}
    # for i in models.Script.objects.all():
    #     if i.device_type not in data1:
    #         data1['{}'.format(i.device_type)] = []
    #         data1['{}'.format(i.device_type)].append([i.id, i.script_name])
    #         continue
    #     if i.device_type in data1:
    #         data1['{}'.format(i.device_type)].append([i.id, i.script_name])
    # context['device'] = data
    # print(data)
    # print(data1)
    # context['script'] = data1
    return render(request, 'index.html', context)


# def test(request):
#     context = {}
#     print(request.method)
#     if request.method == 'POST':
#         # 1.3 获取post除文件外所有数据 -->dict
#         print(request.POST)
#         # 1.4 获取
#         print(request.POST.getlist('ip'))
#     context['hello'] = "'Hello World!'"
#     # context['script'] = ScriptOrm.all()
#     list1 = [{'id': 1, 'type': 2, 'c': 3}, {'id': 11, 'type': 12, 'c': 31}]
#     context['device_num'] = len(list1)
#     context['device'] = json.dumps(list1, indent=2)
#     context['script'] = [{'id': 10, 'type': 20, 'res': 30}, {'id': 11, 'type': 12, 'res': 31}]
#     return JsonResponse(data=context)


def create_input(request):
    data = json.loads(request.body.decode())
    pattern = re.compile(r'<(.*?)>')
    to_action.ids = data
    a = {}
    b = []
    if data['srciptid']:
        # print(i)
        reson = models.Script.objects.get(id=data['srciptid']).script_reson
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
    print(input_data)
    if input_data is not None:
        for d in input_data:
            input_data['{}'.format(d)] = data['{}'.format(d)]
    # print(input_data)
    context = {'ret_data2': []}
    # print(data['srcipt']['name'])
    if data['srciptid']:
        # print(i)
        a = models.Script.objects.get(id=data['srciptid']).script_reson
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

def opaiai(request):
    data = json.loads(request.body.decode('utf-8'))
    context = {}
    # try:
    openai.api_key = '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'
    prompt = data['reason']
    model = "text-davinci-003"
    temperature = 0.5
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=999,
        temperature=temperature,
    )
    time.sleep(1)
    context['data'] = response.choices[0].text
    context['status'] = 200
    # except:
    #     context['status'] = 400
    return JsonResponse(data=context)


def to_data(request):
    context = {}
    # data = request.POST.get('data')
    data = json.loads(request.body.decode())
    data1 = data['deviceid']
    print(data)
    passwd = []
    login = []
    user = []
    port = []
    dtype = []
    reson = to_action.limit_data
    print(reson)
    try:
        for i in data1:
            a = models.Device.objects.get(id=i)
            login.append(a.device_host)
            user.append(a.device_user)
            port.append(a.device_port)
            dtype.append(a.device_type)
            if int(models.Setting.objects.get(setting_name='is_key').setting_value) == 0:
                passwd.append(a.device_passwd)
    except:
        return HttpResponse("数据不存在")
    print(reson)
    print(login)
    print(user)
    print(port)
    print(passwd)
    print(dtype)
    ret_data = to_action.action_ssh(login=login, user=user, passwd=passwd, dtype=dtype,
                                    port=port, script_reson=reson)
    # print('给前端', ret_data)
    context['ret_data1'] = ret_data
    return JsonResponse(data=context)
