import paramiko
from blog import models
from netmiko import ConnectHandler


class Action:
    def __init__(self):
        self.ret = []
        self.is_key = int(models.Setting.objects.get(setting_name='is_key').setting_value)
        self.limit_data = None
        self.input_data = None

    def action_ssh(self, login: list, user: list, port: list, dtype: list, script_reson: list, passwd: list = None):
        if self.is_key == 1:
            for i in range(0, len(login)):
                ret = self.action_ssh_key(login=login[i], user=user[i], port=port[i], cmds=script_reson)
                return ret
        if self.is_key == 0:
            for i in range(0, len(login)):
                if dtype[i] == 'Vyos':
                    ret = self.action_ssh_netmiko(login=login[i], user=user[i],
                                                  port=port[i], cmds=script_reson, password=passwd[i])
                    return ret
                ret = self.action_ssh_passwd(login=login[i], user=user[i],
                                             port=port[i], cmds=script_reson, passwd=passwd[i])
                return ret

    def action_ssh_netmiko(self, login, user, password, port, cmds):
        try:
            conn = ConnectHandler(device_type='vyos',
                                  host=login,
                                  username=user,
                                  password=password,
                                  port=port)
            # ssh_shell = ssh.invoke_shell()
            # ssh = ssh.get_transport().open_session()
            for cmd in cmds:
                if ',' in cmd:
                    for i in cmd.split(","):
                        output = conn.send_command_timing(command_string=i, delay_factor=3)
                        self.ret.append(output)
                    continue
                output = conn.send_command_timing(command_string=cmd, delay_factor=3)
                self.ret.append(output)
        except Exception as err:
            print(err)
        except TimeoutError as err:
            print(err)
        print(self.ret)
        return self.ret

    def action_ssh_key(self, login, user, cmds, port: int = 22):
        # 负责执行
        private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/ipflowser_id_rsa')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=login, username=user, pkey=private_key,
                        port=port, look_for_keys=False)
            # ssh_shell = ssh.invoke_shell()
            for cmd in cmds:
                if ',' in cmd:
                    for i in cmd.split(","):
                        _, out, _ = ssh.exec_command(i)
                        self.ret.append(out.read().decode('utf-8'))
                    continue
                _, out, _ = ssh.exec_command(cmd)
                self.ret.append(out.read().decode('utf-8'))
        except Exception as err:
            print(err)
        except TimeoutError as err:
            print(err)
        print(self.ret)
        return self.ret

    # def ret_data(self, data):
    #     self.ret = data
    #     return self.ret

    def clean_data(self):
        self.ret = []
        self.limit_data = None
        self.input_data = None

    def action_ssh_passwd(self, login, user, passwd, cmds, port: int = 22):
        self.ret = []
        print(login, user, passwd, cmds, port)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=login, username=user, password=passwd,
                        port=port, look_for_keys=False)
            # ssh_shell = ssh.invoke_shell()
            for cmd in cmds:
                if ',' in cmd:
                    for i in cmd.split(","):
                        _, out, _ = ssh.exec_command(i)
                        self.ret.append(out.read().decode('utf-8'))
                    continue
                _, out, _ = ssh.exec_command(cmd)
                self.ret.append(out.read().decode('utf-8'))
        except Exception as err:
            print(err)
        except TimeoutError as err:
            print(err)
        print(self.ret)
        return self.ret
