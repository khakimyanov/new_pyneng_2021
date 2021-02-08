# -*- coding: utf-8 -*-
"""
Задание 18.2b

Скопировать функцию send_config_commands из задания 18.2a и добавить проверку на ошибки.

При выполнении каждой команды, скрипт должен проверять результат на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка, функция должна выводить
сообщение на стандартный поток вывода с информацией о том, какая ошибка возникла,
при выполнении какой команды и на каком устройстве, например:
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1

Ошибки должны выводиться всегда, независимо от значения параметра log.
При этом, параметр log по-прежнему должен контролировать будет ли выводиться сообщение:
Подключаюсь к 192.168.100.1...


Функция send_config_commands теперь должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате (примеры словарей ниже):
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.


Пример работы функции send_config_commands:

In [16]: commands
Out[16]:
['logging 0255.255.1',
 'logging',
 'a',
 'logging buffered 20010',
 'ip http server']

In [17]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Команда "a" выполнилась с ошибкой "Ambiguous command:  "a"" на устройстве 192.168.100.1

In [18]: pprint(result, width=120)
({'ip http server': 'config term\n'
                    'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                    'R1(config)#ip http server\n'
                    'R1(config)#',
  'logging buffered 20010': 'config term\n'
                            'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                            'R1(config)#logging buffered 20010\n'
                            'R1(config)#'},
 {'a': 'config term\n'
       'Enter configuration commands, one per line.  End with CNTL/Z.\n'
       'R1(config)#a\n'
       '% Ambiguous command:  "a"\n'
       'R1(config)#',
  'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

In [19]: good, bad = result

In [20]: good.keys()
Out[20]: dict_keys(['logging buffered 20010', 'ip http server'])

In [21]: bad.keys()
Out[21]: dict_keys(['logging 0255.255.1', 'logging', 'a'])


Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
"""
import yaml
import re
from pprint import pprint
from netmiko import ConnectHandler

# списки команд с ошибками и без:
commands_with_errors = ["logging 0255.255.1", "logging", "a"]
correct_commands = ["logging buffered 20010", "ip http server"]

commands = commands_with_errors + correct_commands

template = 'Команда "{}" выполнилась с ошибкой "{}" на устройстве {}'

#Второй вариант

list_of_mistakes = ['Invalid input detected', 'Incomplete command', 'Ambiguous command']


def send_config_commands(device, config_commands, log=True):
    good_commands = {}
    bad_commands = {}
    
    with ConnectHandler(**device) as ssh:
        if log:
            print("Подключаюсь к {}...".format(device['host']))
        ssh.enable()
        for command in config_commands:
            output = ssh.send_config_set(command)
            if any([mistake in output for mistake in list_of_mistakes]):
                match = re.search(r'% (.*)\.?\n', output)
                if match:
                    print(template.format(command, match.group(1), device['host']))
                    bad_commands[command] = output
            else:
                good_commands[command] = output
        
    return good_commands, bad_commands
"""
Как всегда у Натальи более тонко. Если я проверял, если ли ошибки в строке
    if any([mistake in output for mistake in list_of_mistakes]):
и потом я проверял, а какая именно ошибка
        match = re.search(r'% (.*)\.?\n', output)
            if match:
Наталья сделала проще
    error_in_result = re.seach(r'% (?P<errmsg>.*)', result)
    if error_in_result
т.е. сам факт наличия совпадения будет означать что сообщение об ошибке
было в полученных данных
"""


'''
Первый вариант

regex = (r'% (Invalid input detected.*)'
         r'|% (Incomplete command.*)'
         r'|% (Ambiguous command.*)')

def send_config_commands(device, config_commands, log=True):
    good_commands = {}
    bad_commands = {}
    
    with ConnectHandler(**device) as ssh:
        if log:
            print("Подключаюсь к {}...".format(device['host']))
        ssh.enable()
        for command in config_commands:
            output = ssh.send_config_set(command)
            for line in output.split('\n'):
                match = re.search(regex, output)
                if match:
                    print(template.format(command, match.group(match.lastindex), device['host']))
                    bad_commands[command] = output
                    break
                else:
                    good_commands[command] = output
        
    return good_commands, bad_commands
'''

if __name__ == "__main__":
    
    with open("r1.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        pprint(send_config_commands(dev, commands), width=120)
