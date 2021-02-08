# -*- coding: utf-8 -*-
"""
Задание 19.3

Создать функцию send_command_to_devices, которая отправляет разные
команды show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять
  какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом
команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh int desc
Interface                      Status         Protocol Description
Et0/0                          up             up
Et0/1                          up             up
Et0/2                          admin down     down
Et0/3                          admin down     down
Lo9                            up             up
Lo19                           up             up
R3#sh run | s ^router ospf
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
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

# Этот словарь нужен только для проверки работа кода, в нем можно менять IP-адреса
# тест берет адреса из файла devices.yaml
commands = {
    "192.168.100.1": "sh run | s ^router ospf",
    "192.168.100.2": "sh ip int br",
    "192.168.100.3": "sh int desc",
}


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

#через map и распаковку словаря, но тогда данные в файле упорядочены
#минус в том, что и в словаре commands_dict данные должны быть упорядочены
def send_command_to_devices(devices, commands_dict, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        
        result = executor.map(send_command, devices, [*commands_dict.values()])
        with open(filename, 'w') as dst:
            for device, out in result:
                dst.write(device + out +'\n')

'''
Через submit и обращением напрямую к словарю по значению ключа
def send_command_to_devices(devices, commands_dict, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        
        futures = [executor.submit(send_command, device, commands_dict[device['host']]) for device in devices]
        with open(filename, 'w') as dst:
            for f in as_completed(futures):
                device, out = f.result()
                dst.write(device + out +'\n')
'''
if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    
    send_command_to_devices(devices, commands, 'show_commands_output.txt')
