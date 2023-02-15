import json
import os
import requests
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
# import re
#
# b = 'a <awdadwd-awdfd1<awdsdwd-11'
#
# result = re.findall(r'<(.*?)', b)
#
# if result:
#     for i in result:
#         print(i)
# else:
#     print("No matching content!")
#
#
#
# pattern = re.compile(r'<(.*?)')
#
# match = pattern.findall(b)
#
# if match:
#     for i in match:
#         print(i)

from netmiko import ConnectHandler
import time
import paramiko

# login = '10.10.155.3'
# user = 'testuser'
# password = 'test@123'
# port = 22
# cmds = ['configure t', 'show run']
# times = 30
#

# def ssh_passwd():
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     # try:
#     ssh.connect(hostname=login, username=user, password=password, timeout=times,
#                 port=port, look_for_keys=False)
#     for i in cmds:
#         print(i)
#         _, out, err = ssh.exec_command(i)
#         # if 'configure' in i:
#         #     continue
#         print(out.read().decode('utf-8'))
#         time.sleep(1)
#     ssh.close()
#     #     print('no')
#
#
# ssh_passwd()
# def action_ssh_passwd():
#     ret = []
#     # print(login, user, passwd, cmds, port)
#     try:
#         conn = ConnectHandler(device_type='cisco_ios',
#                               host=login,
#                               username=user,
#                               password=password,
#                               port=port)
#         # ssh_shell = ssh.invoke_shell()
#         # ssh = ssh.get_transport().open_session()
#         for cmd in cmds:
#             output = conn.send_command_timing(command_string=cmd, delay_factor=3)
#
#             print(output)
#     except Exception as err:
#         print(err)
#     except TimeoutError as err:
#         print(err)
#     # print(ret)
#
#
# action_ssh_passwd()
jsond = '''HKG1-SPT1-CNO mtr 45.61.225.1
Start: Wed Feb 15 16:20:52 2023
HOST: HKG1-SPT1-CNO               Loss%   Snt   Last   Avg  Best  Wrst StDev
  1.|-- gateway                   30.0%    10    1.4   0.4   0.2   1.4   0.4
  2.|-- ae10-v962.vr-dsr103-glo1.  0.0%    10    1.2   1.2   0.9   1.8   0.0
  3.|-- lt-0-2023.ls-cr3-he1.jnr1  0.0%    10    1.0   6.6   0.9  56.5  17.5
  4.|-- ve131.core2.hkg1.he.net   90.0%    10    2.1   2.1   2.1   2.1   0.0
  5.|-- 100ge0-76.core3.lax2.he.n 80.0%    10  138.8 140.3 138.8 141.7   2.0
  6.|-- port-channel8.core2.lax1.  0.0%    10  142.0 139.7 138.8 142.0   0.9
  7.|-- 64.71.131.74               0.0%    10  138.8 142.3 138.5 174.6  11.3
  8.|-- 172.16.98.98               0.0%    10  138.7 143.6 138.6 187.5  15.4
  9.|-- 45.61.225.1                0.0%    10  140.4 140.1 139.5 142.6   0.7'''
test = jsond.splitlines()
test1 = []

print(test1)
jsona = {
    "attachments": [
        {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": " w"
                    }
                },
            ]
        }
    ]
}
for i in test:
    jsona['attachments'][0]['blocks'].append({"type": "section", "text": {"type": "plain_text", "text": i.strip()}})

print(jsona)
url = 'https://hooks.slack.com/services/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'
m = json.dumps(jsona, sort_keys=True, indent=2, separators=(',', ':'))
res = requests.post(url, data=m)
print(res)
