# -*- coding: utf-8 -*-
"""
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a
на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них (второй).

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким
образом, чтобы в значении словаря она возвращала список кортежей
для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет
несколько кортежей. Ключом остается имя интерфейса.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность
IP-адреса, диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re
from pprint import pprint
path = "/home/python/github/khakimyanov-9/exercises/15_module_re/"

def get_ip_from_cfg(filename):
    result = {}
    regex = (r'^interface (\S+)'
             r'| ip address (\S+) (\S+)')
            
    with open(filename, 'r') as f:
        for line in f:
            match = re.search(regex, line)
            if match and match.lastindex == 1:
                intf = match.group(1)
            elif match and match.lastindex == 3:
                ip, mask = match.group(2, 3)
                if result.get(intf):
                    result[intf].append((ip, mask))
                else:
                    result[intf] = [(ip, mask)]

    return result

if __name__ == "__main__":
    pprint(get_ip_from_cfg(path + "config_r2.txt"))

'''
опять же можно было использовать именные группы
def get_ip_from_cfg(filename):
    result = {}
    #при таком регулярном выражении в выборку не попадут интерфейсы
    #на который есть description
    regex = (r"interface (?P<intf>\S+)\n"
         r"ip address(?P<ip>\S+) (?<mask>\S+)")
    
    #надо делать как Наталья
    regex = (r"interface (?P<intf>\S+)\n"
             r"(.*\n)*"
             r"ip address(?P<ip>\S+) (?<mask>\S+)"
    )
    #или через pipe
    regex = r"^interface (?P<intf>\S+)\n"
            r"| ip address(?P<ip>\S+) (?<mask>\S+)"
    
    with open(filename) as f:
        for line in f:
            match = re.search(regex, line)
            if match:
                if match.lastgroup == "intf":
                    intf = match.group(match.lastgroup)
                elif match.lastgroup == 'mask':
                    result.setdefault(inft, [])
                    result[intf].append(match.group("ip", "mask"))

'''
'''
# еще один вариант решения

def get_ip_from_cfg(filename):
    result = {}
    with open(filename) as f:
        # сначала отбираем нужные куски конфигурации
        match = re.finditer(
            "interface (\S+)\n"
            "(?: .*\n)*"
            " ip address \S+ \S+\n"
            "( ip address \S+ \S+ secondary\n)*",
            f.read(),
        )
        # потом в этих частях находим все IP-адреса
        for m in match:
            result[m.group(1)] = re.findall("ip address (\S+) (\S+)", m.group())
    return result
'''
