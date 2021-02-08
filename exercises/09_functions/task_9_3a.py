# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
from pprint import pprint

def get_int_vlan_map(config_filename):
    access_ports = {}
    trunk_ports = {}

    with open(config_filename, 'r') as f:
        for line in f:
            if line.startswith('interface'):
                intf = line.split()[-1]
            elif 'access vlan' in line:
                access_ports[intf] = int(line.split()[-1])
            elif 'mode access' in line:
                access_ports[intf] = 1
            elif 'allowed vlan' in line:
                trunk_ports[intf] = [int(vlan) for vlan in line.split()[-1].split(',')]

    return access_ports, trunk_ports


if __name__ == "__main__":
    pprint(get_int_vlan_map('config_sw2.txt'))
