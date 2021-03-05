# -*- coding: utf-8 -*-
"""
Задание 21.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в
параллельных потоках функцию send_and_parse_show_command из задания 21.4.

Параметры функции send_and_parse_command_parallel:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* templates_path - путь к каталогу с шаблонами TextFSM
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать словарь:
* ключи - IP-адрес устройства с которого получен вывод
* значения - список словарей (вывод который возвращает функция send_and_parse_show_command)

Пример словаря:
{'192.168.100.1': [{'address': '192.168.100.1',
                    'intf': 'Ethernet0/0',
                    'protocol': 'up',
                    'status': 'up'},
                   {'address': '192.168.200.1',
                    'intf': 'Ethernet0/1',
                    'protocol': 'up',
                    'status': 'up'}],
 '192.168.100.2': [{'address': '192.168.100.2',
                    'intf': 'Ethernet0/0',
                    'protocol': 'up',
                    'status': 'up'},
                   {'address': '10.100.23.2',
                    'intf': 'Ethernet0/1',
                    'protocol': 'up',
                    'status': 'up'}]}

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
import yaml
from itertools import repeat
from pprint import pprint
from task_21_4 import send_and_parse_show_command
from concurrent.futures import ThreadPoolExecutor, as_completed


def send_and_parse_command_parallel(devices, command, templates_path, limit=3):
    ips = [device['host'] for device in devices]
    
    with ThreadPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(send_and_parse_show_command, devices, repeat(command), repeat(templates_path))
    
    result = dict(zip(ips, list(f_result)))
        
    return result

if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
        
    pprint(send_and_parse_command_parallel(devices, 'sh ip int br', '/home/python/github/khakimyanov-9/exercises/22_textfsm/templates/'))

"""
Наталья сделала через submit
def send_and_parse_command_parallel(devices, command, templates_path, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result_all = [
            executor.submit(send_and_parse_show_command, device, command, templates_path)
            for device in devices
        ]
        output = {device["host"]: f.result() for device, f in zip(devices, result_all)}
    return output

Тут я не совсем понимаю, ведь Submit возвращает результат по мере поступления
и если limit = 2, то есть шанс получить неверные данные при выполнении
    for device, f in zip(devices, result_all)

Получить путь до текущей папки:
path_dir = f"{os.getcwd()}/templates"

"""
