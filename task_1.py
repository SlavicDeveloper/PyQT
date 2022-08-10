import socket
from subprocess import Popen, PIPE
from ipaddress import ip_address
import platform
from socket import gethostbyname


def host_ping(ip_addresses):
    checklst = []
    for ip in ip_addresses:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        args = ["ping", param, '1', str(ip)]
        reply = Popen(args, stdout=PIPE, stderr=PIPE)
        code = reply.wait()

        if code == 0:
            checklst.append(f'узел с {ip} доступен')
        elif code == 1:
            checklst.append(f'Узел с {ip} недоступен')
    return "\n".join(checklst)


def addr_lst_create():
    addr_lst = ['192.168.0.1', '77.88.55.55', 'yandex.ru', 'gsgrbvsf', '77.88.55.55']
    to_host_ping = []
    for el in addr_lst:
        try:
            ipv4 = ip_address(el)
        except ValueError:
            try:
                ipv4 = gethostbyname(el)
            except socket.gaierror:
                print(f'Узел {el} не распознан')
            else:
                to_host_ping.append(ip_address(ipv4))
        else:
            to_host_ping.append(ipv4)
    return addr_lst


print(host_ping(addr_lst_create()))
