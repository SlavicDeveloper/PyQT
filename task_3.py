from subprocess import Popen, PIPE
from ipaddress import ip_address
import platform
from tabulate import tabulate

# 77.88.55.0
from threading import Thread


res_lst = []
threads = []
columns = ["Ip", "Status"]

def host_ping(ip, ):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ["ping", param, '1', str(ip)]
    reply = Popen(args, stdout=PIPE, stderr=PIPE)
    code = reply.wait()
    if code == 0:
        res_lst.append((ip_address(ip), "available"))
    elif code == 1:
        res_lst.append((ip_address(ip), "unavailable"))


def oct_check():
    start_ip = input("Введите стартовое значение ip адреса: ")
    len_of_oct = int(input("Введите значение октета ip адреса: "))
    a = 256 - (int('.'.join(start_ip.split('.')[3:])))
    print(a)
    if a >= len_of_oct:
        addr_create(start_ip, len_of_oct)
    else:
        print("Октет не должен быть более 256 байт. Введите значение еще раз")
        oct_check()


def addr_create(start_ip, len_of_oct):
    i = 0
    iplst = []
    while i <= len_of_oct:
        ipv4 = ip_address(start_ip) + i
        i += 1
        iplst.append(ipv4)
        thread = Thread(target=host_ping, args=(ipv4,))
        thread.start()
        threads.append(thread)

    for thread_it in threads:
        thread_it.join()


oct_check()

print(tabulate(res_lst, headers=columns))
