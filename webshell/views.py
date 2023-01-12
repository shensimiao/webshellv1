from django.shortcuts import render

import json


def index(request):
    context = {}
    print(request.method)
    if request.method == 'POST':
        # 1.3 获取post除文件外所有数据 -->dict
        print(request.POST)
        # 1.4 获取
        print(request.POST.getlist('ip'))
    context['hello'] = 'Hello World!'
    # context['drvice'] = DrviceOrm.all()
    # context['script'] = ScriptOrm.all()
    context['drvice'] = ['001', '002', '003']
    context['script'] = [{'id': 10, 'type': 20, 'res': 30}, {'id': 11, 'type': 12, 'res': 31}]
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
    # context['drvice'] = DrviceOrm.all()
    # context['script'] = ScriptOrm.all()
    list1 = [{'id': 1, 'type': 2, 'c': 3}, {'id': 11, 'type': 12, 'c': 31}]
    context['drvice_num'] = len(list1)
    context['drvice'] = json.dumps(list1, indent=2)
    context['script'] = [{'id': 10, 'type': 20, 'res': 30}, {'id': 11, 'type': 12, 'res': 31}]
    return render(request, 'test.html', context)


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

# def script_resion(request):
#     context = {}
#
