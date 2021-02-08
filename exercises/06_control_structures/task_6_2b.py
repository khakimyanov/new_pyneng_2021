# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

while True:
    ip = input("Введите IP-адрес: ").split('.')
    if not len(ip) == 4 or not all([item.isdigit() for item in ip]) or not all([int(item) in range(0, 256) for item in ip]):
        print("Неправильный IP-адрес")
    else: break
        
if int(ip[0]) in range(1, 224):
    print("unicast")
elif int(ip[0]) in range(224, 240):
    print("multicast")
elif ip == ['255', '255', '255', '255']:
    print("local broadcast")
elif ip == ['0','0','0','0']:
    print("unassigned")
else:
    print("unused")

"""
От Натальи

while True:
    ip = input("Введите IP-адрес в формате x.x.x.x: ")
    octets = ip.split(".")
    valid_ip = len(octets) == 4
    
    for i in octets:
        valid_ip = i.isdigit() and 0 <= int(i) <= 255 and valid_ip
    
    if valid_ip:
        break
    print("Incorrect IPv4 address")

"""
