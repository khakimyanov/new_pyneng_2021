# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess

def ping_ip_addresses(ip_addresses):
    reachable_ips = []
    unreachable_ips = []
    
    for ip in ip_addresses:
        result = subprocess.run(f'ping -c 3 {ip}', shell = True)
        if result.returncode == 0:
            reachable_ips.append(ip)
        else:
            unreachable_ips.append(ip)
    
    return reachable_ips, unreachable_ips

if __name__ == "__main__":
    ip_list = ['8.8.8.8', '80.255.128.1', 'a', '10.1.1.1']
    print(ping_ip_addresses(ip_list))
