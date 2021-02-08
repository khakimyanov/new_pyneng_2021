# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_show_command_to_devices, которая отправляет одну и ту же
команду show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя текстового файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в обычный текстовый файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
"""
import logging
import yaml
from netmiko import ConnectHandler
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint

logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)

def send_command(device, command):
    start_msg = "===> {} Connection: {}"
    received_msg = "<=== {} Received:   {}"
    
    ip = device['host']
    logging.info(start_msg.format(datetime.now().time(), ip))
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        prompt = ssh.find_prompt()
        output = ssh.send_command(command, strip_command=False)
        logging.info(received_msg.format(datetime.now().time(), ip))
    return prompt, output
"""
Наталья
def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        prompt = ssh.find_prompt()
    return f"{prompt}{command}\n{result}\n"

"""

def send_show_command_to_devices(devices, command, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = [executor.submit(send_command, device, command) for device in devices]
        with open(filename, 'w') as dst:
            for f in as_completed(futures):
                device, out = f.result()
                dst.write(device + out +'\n')
"""
Наталья через map
from itertools import repeat

def send_show_command_to_devices(devices, command, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(send_show_command, devices, repeat(command))
        with open(filename, "w") as f:
            for output in results:
                f.write(output)
"""

if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    
    send_show_command_to_devices(devices, 'show clock', 'show_command_output.txt')
