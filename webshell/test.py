import json

context = {}
context['drvice'] = [{'id': 1, 'type': 2, 'c': 3}, {'id': 11, 'type': 12, 'c': 31}]
context['drvice_num'] = len(context['drvice'])
print(json.dumps(context['drvice'],indent=2))
