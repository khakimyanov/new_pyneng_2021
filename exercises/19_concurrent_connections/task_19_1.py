# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
import logging
import netmiko
import subprocess
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint


# эта строка указывает ,что лог-сообщения paramiko юудут выводиться
# только если они уровня WARNING и выше
#logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)
'''
через subprocess.run()
def ip_is_reachable(ipaddr):
    start_msg = "===> {} Connection: {}"
    received_msg = "<=== {} Received:   {}"
    
    logging.info(start_msg.format(datetime.now().time(), ipaddr))
    #чтобы вывод команды Ping не мешал, я направил его в NULL
    result = subprocess.run(f'ping -c 3 {ipaddr}', shell = True, stdout=subprocess.DEVNULL)
    logging.info(received_msg.format(datetime.now().time(), ipaddr))

    if result.returncode == 0:
        return ipaddr, True
    else:
        return ipaddr, False
'''

#реализация с помощью модуля OS

def ip_is_reachable(ipaddr):
    start_msg = "===> {} Connection: {}"
    received_msg = "<=== {} Received:   {}"
    
    logging.info(start_msg.format(datetime.now().time(), ipaddr))
    
    #'> /dev/null 2>&1' аналог 'stdout=subprocess.DEVNULL'
    result = os.system(f'ping -c 3 {ipaddr}' + '> /dev/null 2>&1')
    logging.info(received_msg.format(datetime.now().time(), ipaddr))

    if result == 0:
        return ipaddr, True
    else:
        return ipaddr, False
"""
Как всегда у Натальи более элегантно:
    ip_is_reachable = result.returncode == 0
    return ip_is_reachable

"""


def ping_ip_addresses(ip_list, limit=3):
    reachable_ips = []
    unreachable_ips = []
    
    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = [executor.submit(ip_is_reachable, ipaddr) for ipaddr in ip_list]
    
        for f in as_completed(futures):
            ip, result = f.result()
            if result:
                reachable_ips.append(ip)
            else:
                unreachable_ips.append(ip)
    return reachable_ips, unreachable_ips
"""
Ну и Наталья написала через executor.map()
def ping_ip_addresses(ip_list, limit=3):
    reachable = []
    unreachable = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(ping_ip, ip_list)
    for ip, status in zip(ip_list, results):
        if status:
            reachable.append(ip)
        else:
            unreachable.append(ip)
    return reachable, unreachable

"""

if __name__ == "__main__":
    ip_addresses = ['8.8.8.8', '10.1.1.1', '80.255.128.145', '8.8.4.4', '192.168.1.1', '77.88.8.8', '1.1.1.1', '172.16.1.5']
    pprint(ping_ip_addresses(ip_addresses))
