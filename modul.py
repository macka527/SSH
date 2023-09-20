import paramiko
from time import monotonic as _time
import time

host = "10.128.0.126"
username = "huaweitftp"
password = "Qwerty123Qwerty"

class SOM():
    def __init__(
        self,        
        host,
        user,
        password,
        ):      
        self.host = host
        self.user = user
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.host, username=self.user, password=self.password)
        self.ssh = self.client.invoke_shell()    

    def read_until_ssh(self, param1, param2='-None-', timeout=None):      
        # all_b список для записи всех собранных байт
        all_b = []
        # Проверяет создан ли таймер, если создан монтирует точку отсчета deadline
        if timeout is not None:
            deadline = _time() + timeout

        while True:
            time.sleep(0.1)
            # проверяем есть ли байты готовые к получению
            sad = self.ssh.recv_ready()
            if sad is True:
                # если есть байты готовые к получению, собираем их и записываем в all_b
                b = self.ssh.recv(3000).decode('utf-8')
                all_b.append(b)

                # проверяем найден ли хотя бы один из параметров
                if (param1 in b) or (param2 in b):                
                    break
                # проверяем таймер
                if timeout is not None:
                    timeout = deadline - _time()
                    if timeout < 0:
                        all_b.append('timeout')
                        break
            elif sad is False:
                # если нет байт готовых к получению, проверяем таймер
                # проверяем таймер
                if timeout is not None:
                    timeout = deadline - _time()
                    if timeout < 0:
                        all_b.append('timeout')
                        break
        return all_b

    def write_ssh(self, text):
        self.ssh.send(text)

    def close_ssh(self):
        self.client.close()

    def recv_ssh(self):
        time.sleep(0.1)
        b = self.ssh.recv(3000).decode('utf-8')
        return b


if __name__ == '__main__':
    ssh1 = SOM(host, username, password)
    ssh1.recv_ssh()

    ssh1.write_ssh('display saved-configuration time\n')
    text = ssh1.read_until_ssh('Info:Current configuration has not been saved automatically since system booted or slave switchover', timeout=10)
    print(text)
    ssh1.close_ssh()
