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

login = '10.10.155.3'
user = 'testuser'
password = 'test@123'
port = 22
cmds = ['configure t', 'show run']
times = 30


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
def action_ssh_passwd():
    ret = []
    # print(login, user, passwd, cmds, port)
    try:
        conn = ConnectHandler(device_type='cisco_ios',
                              host=login,
                              username=user,
                              password=password,
                              port=port)
        # ssh_shell = ssh.invoke_shell()
        # ssh = ssh.get_transport().open_session()
        for cmd in cmds:
            output = conn.send_command_timing(command_string=cmd, delay_factor=3)

            print(output)
    except Exception as err:
        print(err)
    except TimeoutError as err:
        print(err)
    # print(ret)


action_ssh_passwd()
