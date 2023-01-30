import os

import django
from django.shortcuts import render, HttpResponse
from requests import request
from lib.action import Action
from blog import models
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webshell.settings")  # project_name指项目名
django.setup()
to_action = Action()


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
    data = {}
    for i in models.Drvice.objects.all():
        if i.drvice_type not in data:
            data['{}'.format(i.drvice_type)] = []
            data['{}'.format(i.drvice_type)].append(i.drvice_name)
            continue
        if i.drvice_type in data:
            data['{}'.format(i.drvice_type)].append(i.drvice_name)
    data1 = {}
    for i in models.Script.objects.all():
        if i.drvice_type not in data1:
            data1['{}'.format(i.drvice_type)] = []
            data1['{}'.format(i.drvice_type)].append(i.script_name)
            continue
        if i.drvice_type in data1:
            data1['{}'.format(i.drvice_type)].append(i.script_name)
    context['drvice'] = data
    print(data)
    print(data1)
    context['script'] = data1
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
    return render(request, 'test.html', context)


# def drvice_add(requset):
#     models.Drvice.objects.create(drvice_name='hkd1-dev6', drvice_host='192.168.11.2', drvice_type='HK',
#                                  drvice_port='22')
#     all = models.Drvice.objects.filter(drvice_type='HK')
#     return HttpResponse(all)


# def search(request):
#     ss = request.POST.get('search')  # 获取搜索的关键词
#     list = Article.objects.filter(title__icontains=ss)  # 获取到搜索关键词通过标题进行匹配
#     remen = Article.objects.filter(tui__id=2)[:6]
#     allcategory = Category.objects.all()
#     page = request.POST.get('page')
#     tags = Tag.objects.all()
#     paginator = Paginator(list, 10)
#     try:
#         list = paginator.page(page)  # 获取当前页码的记录
#     except PageNotAnInteger:
#         list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
#     except EmptyPage:
#         list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
#     return render(request, 'search.html', locals())

def to_data(request):
    context = {}
    # data = request.POST.get('data')
    data = json.loads(request.body.decode())
    ip = data['ip']
    network = data['network']
    data1 = data['drvice']
    data2 = data['srcipt']
    reson = ['conf t']
    passwd = []
    login = []
    user = []
    port = []
    for i in data2:
        reson.append(models.Script.objects.get(script_name='{}'.format(i)).script_reson)
    for i in data1:
        a = models.Drvice.objects.get(drvice_name='{}'.format(i))
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
    print('给前端', ret_data)
    context['ret_data1'] = ret_data
    return render(request, 'index.html', context)


def to_reson(request):
    print(request.method)
    # print(request.GET)
    # data = request.POST.get('srcipt')
    data = json.loads(request.body.decode())
    # print('返回', data)
    # data = dict(data)
    ip = data['ip']
    network = data['network']
    context = {'ret_data2': ''}
    # print(data['srcipt']['name'])
    for i in data['srcipt']['name']:
        # print(i)
        context['ret_data2'] = context['ret_data2'] + '\n' + models.Script.objects.get(
            script_name='{}'.format(i)).script_reson.replace('<ip>', ip).replace('<network>', network)
    # print(context['ret_data'])
    return render(request, 'index.html', context)


def clean_all(request):
    to_action.clean_data()
    context = {"ret_data1": '', "ret_data2": '', }
    # return render(request, 'index.html', context)
    return render(request, 'index.html', context)
