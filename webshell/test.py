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

jsond = {
    "data": [
        {
            "name": "srcipt",
            "children": [
                {
                    "name": "Vyos",
                    "children": [
                        {
                            "name": "查看全局配置",
                            "id": 1
                        },
                        {
                            "name": "查看接口",
                            "id": 3
                        },
                        {
                            "name": "查看指定路由详细信息",
                            "id": 4
                        },
                        {
                            "name": "查看OSPF路由表",
                            "id": 5
                        },
                        {
                            "name": "查看OSPF邻居状态",
                            "id": 6
                        },
                        {
                            "name": "查看BGP汇总信息",
                            "id": 7
                        },
                        {
                            "name": "查看指定BGP路由详细信息",
                            "id": 8
                        },
                        {
                            "name": "查看BGP邻居发送过来的路由",
                            "id": 9
                        },
                        {
                            "name": "使用指定接口IP ping目的地址",
                            "id": 10
                        },
                        {
                            "name": "使用指定源IP traceroute 目标IP",
                            "id": 11
                        },
                        {
                            "name": "查看日志",
                            "id": 12
                        },
                        {
                            "name": "创建新用户",
                            "id": 44
                        }
                    ]
                },
                {
                    "name": "cisco",
                    "children": [
                        {
                            "name": "show run",
                            "id": 2
                        },
                        {
                            "name": "查看全局配置",
                            "id": 24
                        },
                        {
                            "name": "查看接口描述",
                            "id": 25
                        },
                        {
                            "name": "查看指定路由详细信息",
                            "id": 26
                        },
                        {
                            "name": "查看OSPF路由表",
                            "id": 27
                        },
                        {
                            "name": "查看OSPF邻居状态",
                            "id": 28
                        },
                        {
                            "name": "查看BGP汇总信息",
                            "id": 29
                        },
                        {
                            "name": "查看指定BGP路由详细信息",
                            "id": 30
                        },
                        {
                            "name": "查看BGP邻居发送过来的路由",
                            "id": 31
                        },
                        {
                            "name": "ping",
                            "id": 32
                        },
                        {
                            "name": "traceroute",
                            "id": 33
                        },
                        {
                            "name": "查看日志",
                            "id": 34
                        },
                        {
                            "name": "创建新用户",
                            "id": 46
                        },
                        {
                            "name": "测试用例",
                            "id": 47
                        }
                    ]
                },
                {
                    "name": "juniper",
                    "children": [
                        {
                            "name": "查看全局配置",
                            "id": 13
                        },
                        {
                            "name": "查看接口简要信息",
                            "id": 14
                        },
                        {
                            "name": "查看指定路由详细信息",
                            "id": 15
                        },
                        {
                            "name": "查看指定路由详细信息",
                            "id": 16
                        },
                        {
                            "name": "查看OSPF路由表",
                            "id": 17
                        },
                        {
                            "name": "查看BGP汇总信息",
                            "id": 18
                        },
                        {
                            "name": "查看指定BGP路由信息",
                            "id": 19
                        },
                        {
                            "name": "查看BGP邻居发送过来的路由",
                            "id": 20
                        },
                        {
                            "name": "使用指定源IP ping 目标IP",
                            "id": 21
                        },
                        {
                            "name": "使用指定源IP traceroute 目标IP",
                            "id": 22
                        },
                        {
                            "name": "查看日志并过滤显示指定内容",
                            "id": 23
                        },
                        {
                            "name": "创建新用户",
                            "id": 45
                        }
                    ]
                },
                {
                    "name": "ROS",
                    "children": [
                        {
                            "name": "查看全局配置",
                            "id": 35
                        },
                        {
                            "name": "查看网卡接口",
                            "id": 36
                        },
                        {
                            "name": "查看IP",
                            "id": 37
                        },
                        {
                            "name": "查看ARP表并模糊过滤指定mac地址",
                            "id": 38
                        },
                        {
                            "name": "查看IP表并模糊过滤指定接口",
                            "id": 39
                        },
                        {
                            "name": "查看Route表并模糊过滤指定IP地址",
                            "id": 40
                        },
                        {
                            "name": "使用Traceroute工具",
                            "id": 41
                        },
                        {
                            "name": "使用Ping工具",
                            "id": 42
                        },
                        {
                            "name": "查看日志",
                            "id": 43
                        }
                    ]
                }
            ]
        }
    ]
}
print(type(jsond))
ds = str(jsond)
# print(ds)
# print(ds.find("'id': 41"))
dt = ds.replace("'id': 2}", "'id': 2, 'disable': True}")
print(dt)
dt = eval(dt)
print(json.dumps(dt))