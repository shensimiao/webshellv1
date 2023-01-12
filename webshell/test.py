import json
import os

import django

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webshell.settings")  # project_name指项目名
django.setup()
context = {}
context['drvice'] = [{'id': 1, 'type': 2, 'c': 3}, {'id': 11, 'type': 12, 'c': 31}]
context['drvice_num'] = len(context['drvice'])
print(json.dumps(context['drvice'],indent=2))
