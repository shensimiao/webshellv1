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

a = {}
b = ["\r\nBuilding configuration...\r\n\r\n  \r\nCurrent configuration : 3463 bytes\r\n!\r\n! Last configuration change at 06:21:10 UTC Fri Feb 17 2023\r\n!\r\nversion 15.9\r\nservice timestamps debug datetime msec\r\nservice timestamps log datetime msec\r\nno service password-encryption\r\n!\r\nhostname CS1-AS801\r\n!\r\nboot-start-marker\r\nboot-end-marker\r\n!\r\n!\r\nenable secret 9 $9$4mhL1xK8PfInff$ceUlQIL6SHlTNEqhMGLOaZiGOalpa51tyHp5l7UPKH2\r\n!\r\nno aaa new-model\r\n!\r\n!\r\n!\r\nmmi polling-interval 60\r\nno mmi auto-configure\r\nno mmi pvc\r\nmmi snmp-timeout 180\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\nno ip domain lookup\r\nip domain name cisco\r\nip cef\r\nno ipv6 cef\r\n!\r\nmultilink bundle-name authenticated\r\n!\r\n!\r\n!\r\n!\r\nusername testuser privilege 15 secret 9 $9$IqnqCVW8l4TE8f$x4hpvtm/SbawxAmj8rVqrQRKpuw8.dwxbl1odDGRq6M\r\n!\r\nredundancy\r\n!\r\n!\r\n! \r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r\ninterface GigabitEthernet0/0\r\n no ip address\r\n duplex auto\r\n speed auto\r\n media-type rj45\r\n!\r\ninterface GigabitEthernet0/1\r\n description GW1-eth2\r\n ip address 200.99.1.2 255.255.255.252\r\n duplex auto\r\n speed auto\r\n media-type rj45\r\n!\r\ninterface GigabitEthernet0/2\r\n ip address 10.10.155.13 255.255.255.0\r\n duplex auto\r\n speed auto\r\n media-type rj45\r\n!\r\ninterface GigabitEthernet0/3\r\n no ip address\r\n shutdown\r\n duplex auto\r\n speed auto\r\n media-type rj45\r\n!\r\nip forward-protocol nd\r\n!\r\n!\r\nno ip http server\r\nno ip http secure-server\r\nip route 0.0.0.0 0.0.0.0 200.99.1.1\r\nip route 10.10.0.0 255.255.0.0 10.10.155.1\r\nip route 10.65.0.0 255.255.0.0 10.10.155.1\r\nip route 10.75.0.0 255.255.0.0 10.10.155.1\r\nip route 10.85.0.0 255.255.0.0 10.10.155.1\r\nip ssh time-out 60\r\nip ssh version 2\r\n!\r\nipv6 ioam timestamp\r\n!\r\n!\r\n!\r\ncontrol-plane\r\n!\r\nbanner exec ^C\r\n**************************************************************************\r\n* IOSv is strictly limited to use for evaluation, demonstration and IOS  *\r\n* education. IOSv is provided as-is and is not supported by Cisco's      *\r\n* Technical Advisory Center. Any use or disclosure, in whole or in part, *\r\n* of the IOSv Software or Documentation to any third party for any       *\r\n* purposes is expressly prohibited except as otherwise authorized by     *\r\n* Cisco in writing.                                                      *\r\n**************************************************************************^C\r\nbanner incoming ^C\r\n**************************************************************************\r\n* IOSv is strictly limited to use for evaluation, demonstration and IOS  *\r\n* education. IOSv is provided as-is and is not supported by Cisco's      *\r\n* Technical Advisory Center. Any use or disclosure, in whole or in part, *\r\n* of the IOSv Software or Documentation to any third party for any       *\r\n* purposes is expressly prohibited except as otherwise authorized by     *\r\n* Cisco in writing.                                                      *\r\n**************************************************************************^C\r\nbanner login ^C\r\n**************************************************************************\r\n* IOSv is strictly limited to use for evaluation, demonstration and IOS  *\r\n* education. IOSv is provided as-is and is not supported by Cisco's      *\r\n* Technical Advisory Center. Any use or disclosure, in whole or in part, *\r\n* of the IOSv Software or Documentation to any third party for any       *\r\n* purposes is expressly prohibited except as otherwise authorized by     *\r\n* Cisco in writing.                                                      *\r\n**************************************************************************^C\r\n!\r\nline con 0\r\n logging synchronous\r\nline aux 0\r\nline vty 0 4\r\n login local\r\n transport input ssh\r\n!\r\nno scheduler allocate\r\n!\r\nend\r\n", 'error1:']

c = [4, 5, 6]
v = '65165'
b.insert(0, '{}\r\n'.format(v))
print(b)
