# -*- coding: utf-8 -*-
"""
Задание 15.1

Создать функцию get_ip_from_cfg, которая ожидает как аргумент имя файла,
в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать IP-адреса и маски,
которые настроены на интерфейсах, в виде списка кортежей:
* первый элемент кортежа - IP-адрес
* второй элемент кортежа - маска

Например (взяты произвольные адреса):
[('10.0.1.1', '255.255.255.0'), ('10.0.2.1', '255.255.255.0')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.


Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re

def get_ip_from_cfg(filename):
    result = []
    regex = r"ip address (\S+) (\S+)"
    
    with open(filename, 'r') as f:
        for line in f:
            match = re.search(regex, line)
            if match:
                ip, mask = match.groups()
                result.append((ip, mask))
    return result

if __name__ == "__main__":
    print(get_ip_from_cfg("config_r1.txt"))

'''
я плохо понял findall и finditer поэтому не использова их в решении.
Но в прошлый раз я сделал это задание с findall

regex = r'ip address (\S+) (\S+)'

with open(filename) as f:
    matches = re.findall(regex, f.read())
    
а Наталья предложила решение с finditer
regex = r'ip address (\S+) (\S+)'
with open(filename) as f:
    result = [m.groups() for m in re.finditer(regex, f.read())]
    
'''
