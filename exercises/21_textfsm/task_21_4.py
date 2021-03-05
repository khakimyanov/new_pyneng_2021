# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
import yaml
import os
import logging
from netmiko import ConnectHandler
from datetime import datetime
from pprint import pprint

# эта строка указывает ,что лог-сообщения paramiko юудут выводиться
# только если они уровня WARNING и выше
logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_and_parse_show_command(device_dict, command, templates_path, index='index'):
    start_msg = "===> {} Connection: {}"
    received_msg = "<=== {} Received:   {}"
    
    if "NET_TEXTFSM" not in os.environ:
        os.environ['NET_TEXTFSM'] = templates_path
    
    ip = device_dict['host']
    logging.info(start_msg.format(datetime.now().time(), ip))
    
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        output = ssh.send_command(command, use_textfsm=True)
        logging.info(received_msg.format(datetime.now().time(), ip))

    return output
    
if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
            
    for device in devices:
        pprint(send_and_parse_show_command(device, 'sh ip int br', '/home/python/github/khakimyanov-9/exercises/22_textfsm/templates/'))

"""
Для получения полного пути Наталья предлагает использовать
    full_pth = os.path.join(os.getcwd(), "templates")
"""
