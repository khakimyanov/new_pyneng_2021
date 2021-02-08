# -*- coding: utf-8 -*-
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

"""
import re
from pprint import pprint

def parse_sh_ip_int_br(filename):
    result = []
    regex = r"(\S+) +(\S+) +\S+ +\S+ +(up|down|administratively down) +(up|down)"
    
    with open(filename, 'r') as f:
        for line in f:
            match = re.search(regex, line)
            if match:
                result.append(match.groups())
    return result

if __name__ == "__main__":
    pprint(parse_sh_ip_int_br("sh_ip_int_br.txt"))

'''
опять же с findall/finditer нам не нужно определять переменную result и не делать лишний
цикл if match
def parse_sh_ip_int_br(filename):
    regex = r"(\S+) +(\S+) +\S+ +\S+ +(up|administratively down) +(up|down)"
    
    with open(filename) as f:
        matches = re.findall(regex, f.read())
    
    return matches

Тоже самое через finditer
def parse_sh_ip_int_br(textfile):
    regex = r"(\S+) +(\S+) +\w+ \w+ +(administratively down|up|down) +(up|down)"
    with open(textfile) as f:
        result = [m.groups() for m in re.finditer(regex, f.read())]
    return result

'''
