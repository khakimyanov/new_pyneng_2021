# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re
from pprint import pprint

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
                result[intf] = (ip, mask)

    return result

if __name__ == "__main__":
    pprint(get_ip_from_cfg("config_r1.txt"))

'''
Наталья предлогает использовать именные группы
def get_ip_from_cfg(config):
    with open)config) as f:
        regex = re.compile(
            r"interface (?P<intf>\S+)\n"          #interface
            r"( .*\n)*"                           #возможно description
            r"ip address(?P<ip>\S+) (?<mask>\S+)" #IP and mask
        )
        match = regex.finditer(f.read())
    result = {m.group("intf"): m.group("ip", "mask") for m in match}
    
    return result
'''
