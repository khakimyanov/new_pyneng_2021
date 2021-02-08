# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
template = "{:<4}    {}  {}"
mac_table = []

with open("CAM_table.txt", 'r') as f:
	for line in f:
		if line.strip() and line.split()[0].isdigit():
		    vlan, mac, _, intf = line.split()
		    mac_table.append((int(vlan), mac, intf))

vlan_id = input("Введите номер VLAN: ")

for item in sorted(mac_table):
	if item[0] == int(vlan_id):
	    print(template.format(*item))
