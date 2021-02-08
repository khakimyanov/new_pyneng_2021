# -*- coding: utf-8 -*-
"""
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости
от выбранного режима, задавались разные вопросы в запросе о номере
VLANа или списка VLANов:
* для access: 'Введите номер VLAN:'
* для trunk: 'Введите разрешенные VLANы:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
"""

access_template = [
    "switchport mode access",
    "switchport access vlan {}",
    "switchport nonegotiate",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
]

trunk_template = [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan {}",
]

template_dict = {'access': '\n'.join(access_template), 'trunk': '\n'.join(trunk_template)}
question = {'access': "Введите номер VLAN: ", 'trunk': "Введите разрешенные VLANы: "}

vlan_mode = input("Введите режим работы интерфейса (access/trunk): ")
intf = input("Введите тип и номер интерфейса: ")
vlans = input(question[vlan_mode])

print("interface {}".format(intf))
print(template_dict[vlan_mode].format(vlans))
