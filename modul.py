import paramiko
import time
from time import monotonic as _time

class My_Telnetlib():
    """
    Заходит на SSH сервер по закрытому ключу и выполняет подключения Telnet с этого сервера
    """
    def __init__(
        self,        
        ip,
        host_ssh,
        user_ssh,
        your_ip,
        ):
        self.ip = ip, # host for telnet
        self.host_ssh = host_ssh
        self.user_ssh = user_ssh
        self.your_ip = your_ip
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())       
        self.client.connect(hostname=self.host_ssh, username=self.user_ssh)
        self.ssh = self.client.invoke_shell()
        self.ssh_telnet_connect()
    
    def ssh_telnet_connect(self, timeout=10):
        self.ssh.send(f"telnet {self.ip[0]}\n")
        deadline = _time() + timeout
        a = '-'        
        while a:            
            if 'Connected to' in a:
                a = True
                break            
            elif ('onnection refused' in a) or ('onnection timed out' in a):                
                del a
                break
            else:
                sad = self.ssh.recv_ready()
                if sad is True:
                    a = self.ssh.recv(3000).decode('utf-8')
                elif sad is False:
                    pass                  
            timeout = deadline - _time()
            if timeout < 0:
                del a
                break
        return a

    def read_until_ssh(self, param1, param2='-None-', timeout=None):       
        all_b = []
        b = self.ssh.recv(3000).decode('utf-8')        
        if self.your_ip in b:
            b = '-'
        else:
            all_b.append(b)        
        if timeout is not None:
            deadline = _time() + timeout            
        while b:
            if (param1 in b) or (param2 in b) :                
                    break                
            else:
                sad = self.ssh.recv_ready()                
                if sad is True:
                    b = self.ssh.recv(3000).decode('utf-8')                                  
                    all_b.append(b)
                elif sad is False:
                    pass
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
        time.sleep(0.2)
        b = self.ssh.recv(3000).decode('utf-8')
        return b





    
if __name__=="__main__":    
    pass

    