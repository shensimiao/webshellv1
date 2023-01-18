import paramiko
from blog import models


class Action:
    def __init__(self):
        self.ret = None
        self.is_key = None

    def action_ssh(self, login: list, user: list, port: list, script_reson: list, passwd: list = None):
        if self.is_key == 1:
            for i in range(0, len(login)):
                self.action_ssh_key(login=login[i], user=user[i], port=port[i], cmds=script_reson)
        if self.is_key == 0:
            for i in range(0, len(login)):
                self.action_ssh_passwd(login=login[i], user=user[i],
                                       port=port[i], cmds=script_reson, passwd=passwd[i])

    def action_ssh_key(self, login, user, cmds, port: int = 22):
        # 负责执行
        private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/ipflowser_id_rsa')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=login, username=user, pkey=private_key,
                        port=port, look_for_keys=False)
            ssh_shell = ssh.invoke_shell()
            for cmd in cmds:
                ssh_shell.send(cmd + '\n')
                ret = ssh_shell.recv(1024).decode('utf-8')
                self.ret_data(ret)
        except Exception as err:
            print(err)
        except TimeoutError as err:
            print(err)

    def ret_data(self, data):
        self.ret = self.ret + '\n' + data
        return self.ret

    def clean_data(self):
        self.ret = None
        pass

    def action_ssh_passwd(self, login, user, passwd, cmds, port: int = 22):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=login, username=user, password=passwd,
                        port=port, look_for_keys=False)
            ssh_shell = ssh.invoke_shell()
            for cmd in cmds:
                ssh_shell.send(cmd + '\n')
                ret = ssh_shell.recv(1024).decode('utf-8')
                self.ret_data(ret)
        except Exception as err:
            print(err)
        except TimeoutError as err:
            print(err)
