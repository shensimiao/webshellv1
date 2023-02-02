import json
import os

import django

import os, django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webshell.settings")  # project_name指项目名
# django.setup()
# context = {}
# context['drvice'] = [{'id': 1, 'type': 2, 'c': 3}, {'id': 11, 'type': 12, 'c': 31}]
# # context['drvice_num'] = len(context['drvice'])
# # print(json.dumps(context['drvice'],indent=2))
# a = [1, 2, 3]
# for i in range(0, len(a)):
#     print(a[i])
#     print(i)

# # print(a)
# # list(a)
# # print(a)
# if 'ds' not in context:
#     context['ds'] = []
#     context['ds'].append('a')
# if 'ds' in context:
#     context['ds'].append('v')
#
# print(context['ds'])
# print(int('0'))
# a.append({"ad":"{}".format(b)})
import re

b = 'a <awdadwd-awdfd1><awdsdwd-11>'

result = re.findall(r'<(.*?)>', b)

if result:
    for i in result:
        print(i)
else:
    print("No matching content!")



pattern = re.compile(r'<(.*?)>')

match = pattern.findall(b)

if match:
    for i in match:
        print(i)