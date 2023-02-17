import paramiko
from blog import models
from netmiko import ConnectHandler


class Action:
    def __init__(self):
        self.ret = []
        self.is_key = int(models.Setting.objects.get(setting_name='is_key').setting_value)
        self.limit_data = None
        self.input_data = None
        self.srcipt_true = None
        self.device_true = None
        self.ids = None

    def action_ssh(self, login: list, user: list, port: list, dtype: list, script_reson: list, passwd: list = None):
        data = {}
        if self.is_key == 1:
            for i in range(0, len(login)):
                ret = self.action_ssh_key(login=login[i], user=user[i], port=port[i], cmds=script_reson)
                data['{}'.format(login[i])] = ret
            # print(data)
            return data
        if self.is_key == 0:
            if dtype[0] == 'Vyos':
                for i in range(0, len(login)):
                    ret = self.action_ssh_netmiko(login=login[i], user=user[i],
                                                  port=port[i], cmds=script_reson, password=passwd[i])
                    print('{}'.format(login[i]) + str(ret))
                    data['{}'.format(login[i])] = ret

                return data
            for i in range(0, len(login)):
                ret = self.action_ssh_passwd(login=login[i], user=user[i],
                                             port=port[i], cmds=script_reson, passwd=passwd[i])
                data['{}'.format(login[i])] = ret
            # print(data)
            return data

    def action_ssh_netmiko(self, login, user, password, port, cmds):
        ret = []
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
                        ret.append(output)
                        # print(i, output)
                    continue
                output = conn.send_command_timing(command_string=cmd, delay_factor=3)
                ret.append(output)
                # print(cmd, output)
            conn.close_session_log()
        except TimeoutError as err:
            # print('error2:', err)
            ret.append('error2:' + err.strerror)
            # print(ret)
            return ret
        except OSError as err:
            # print('error3:', err)
            ret.append('error3:' + err.strerror)
            # print(ret)
            return ret
        except paramiko.ssh_exception.SSHException as err:
            # print('error4:', err)
            ret.append('error4:{}'.format(err))
            # print(ret)
            return ret
        except Exception as err:
            # print('error1:', err)
            ret.append('error1:{}'.format(err))
            # print(ret)
            return ret
        except:
            pass
        # print(ret)
        return ret

    def action_ssh_key(self, login, user, cmds, port: int = 22):
        # 负责执行
        ret = []
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
                        # print(i, out.read())
                    continue
                _, out, _ = ssh.exec_command(cmd)
                self.ret.append(out.read().decode('utf-8'))
                # print(cmd, out.read())
            ssh.close()
        except TimeoutError as err:
            # print('error2:', err)
            ret.append('error2:' + err.strerror)
        except OSError as err:
            # print('error3:', err)
            ret.append('error3:' + err.strerror)
        except paramiko.ssh_exception.SSHException as err:
            # print('error4:', err)
            ret.append('error4:{}'.format(err))
        except Exception as err:
            # print('error1:', err)
            ret.append('error1:{}'.format(err))

        return ret

    # def ret_data(self, data):
    #     self.ret = data
    #     return self.ret

    def clean_data(self):
        self.ret = []
        self.limit_data = None
        self.input_data = None

    def action_ssh_passwd(self, login, user, passwd, cmds, port: int = 22):
        ret = []
        print(login, user, passwd, cmds, port)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=login, username=user, password=passwd,
                        port=port, look_for_keys=False)
            # ssh_shell = ssh.invoke_shell()
            for cmd in cmds:
                if ',' not in cmd:
                    _, out, _ = ssh.exec_command(cmd)
                    if 'configure' in cmd:
                        continue
                    ret.append(out.read().decode('utf-8'))
                data = cmd.split(',')
                for i in range(0, len(data)):
                    _, out, _ = ssh.exec_command(data[i])
                    ret.append(out.read().decode('utf-8'))
                    # print(data[i])
            ssh.close()
        except TimeoutError as err:
            # print('error2:', err)
            ret.append('error2:' + err.strerror)
        except OSError as err:
            # print('error3:', err)
            ret.append('error3:' + err.strerror)
        except paramiko.ssh_exception.SSHException as err:
            # print('error4:', err)
            ret.append('error4:{}'.format(err))
        except Exception as err:
            # print('error1:', err)
            ret.append('error1:{}'.format(err))

        # print(ret)
        return ret
