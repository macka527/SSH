# SSH
from ssh.modul import SOM

host = "localhost"
username = "testuser"
password = "testpass"

if __name__ == '__main__':
    ssh = SOM(host, username, password)
    ssh.recv_ssh()
    ssh.write_ssh('display saved-configuration time\n')
    text = ssh.read_until_ssh('#', ']', timeout=10)
    print(text)
    ssh1.close_ssh()
