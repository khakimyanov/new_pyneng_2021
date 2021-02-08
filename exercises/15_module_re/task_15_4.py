# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
"""
import re
from pprint import pprint

'''
тут тоже не удалось уйти от создания словаря, но покрайней мере он не 
заполняется значениями
'''
def get_ints_without_description(filename):
    _result = {}
    regex = (r'^interface (\S+)'
             r'| description (.+)')
    
    with open(filename, 'r') as f:
        for line in f:
            match = re.search(regex, line)
            if match and match.lastindex == 1:
                intf = match.group(1)
                _result[intf] = None
            elif match and match.lastindex == 2:
                del _result[intf]
            
    return list(_result)       


'''
Это решение мне не очень нравиться, так как избыточно создаеся словарь,
заполняется и только потом из него создается список

def get_ints_without_description(filename):
    _result = {}
    regex = (r'^interface (\S+)'
             r'| description (.+)')
             
    with open(path + filename, 'r') as f:
        for line in f:
            match = re.search(regex, line)
            if match and match.lastindex == 1:
                intf = match.group(1)
                _result[intf] = None
            elif match and match.lastindex == 2:
                _result[intf] = match.group(2)
    
    return [item for item in _result if not _result[item]]
'''
    
if __name__ == "__main__":
    pprint(get_ints_without_description("config_r1.txt"))
    
"""
в прошлый раз я сам сделал решение через списки

def get_ints_without_description(filename):
    result = []
    regex = (r'^interface (?P<intf>\S+)'
             r'| description (?P<desc>.+)')
    
    with open(path + filename, 'r') as f:
        for line in f:
            match = re.search(regex, line)
            if match and match.lastgroup == 'intf':
                intf = match.group('intf')
                result.append(intf)
            elif match and match.lastgroup == 'desc':
                result.remove(intf)
            
    return result       

Наталья как всегда предложела более короткое решение
def get_ints_without_description(filename):
    regex = re.compile(r"!\ninterface (?P<intf>\S+)"
                       r"(?P<desc> description \S+)?")
    with open(config) as scr:
        match = regex.finditer(src.read())
        result = [m.group('intf') for m in match if m.lastgroup == 'intf']
        return result

"""
