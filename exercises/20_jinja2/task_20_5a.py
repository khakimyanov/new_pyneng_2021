# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""
import re
import natsort
from task_20_5 import create_vpn_config
from netmiko import ConnectHandler
from pprint import pprint

data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    
    # следующее значение номера туннеля на основании уже имеющихся туннелей
    data['tun_num'] =  parse_scr_dst_configs(src_device_params, dst_device_params)

    #создаем шаблоны
    scr_config, dst_config = create_vpn_config(src_template, dst_template, vpn_data_dict)
    
    #так как шаблоны - это строка, а функция netmiko.send_config_set запрашивает список,
    #используем split('\n')
    return send_config_commands(src_device_params, scr_config.split('\n')), send_config_commands(dst_device_params, dst_config.split('\n'))

def parse_scr_dst_configs(local_dev, remote_dev):
    '''
    функция получает параметры устройст, запрашивает вывод 'sh ip int br |  include Tunnel'
    и, используя функцию tunnel_number_is(), получает максиммальное значение номера уже 
    существующих туннелей, прибавляя к нему 1
    '''
    local_sh_ip_int_br = send_show_command(local_dev, 'sh ip int br |  include Tunnel')
    remote_sh_ip_int_br = send_show_command(remote_dev,'sh ip int br | include Tunnel')
    
    #если вывод 'sh ip int br |  include Tunnel' пустой, то следовательно
    #номер туннеля - 0
    if not local_sh_ip_int_br and not remote_sh_ip_int_br:
        return '0'
    else:
        return tunnel_number_is(local_sh_ip_int_br, remote_sh_ip_int_br)

def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        return ssh.send_command(command)

def send_config_commands(device, commands):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        return ssh.send_config_set(commands)
    
def tunnel_number_is(local_sh_ip_int_br, remote_sh_ip_int_br):
    '''
    Получаем сортированный список всех всех номеров туннелей (в виде строк), 
    берем последнее (максимальное) значение, так как полученный элемент -
    это строка, поэтому применяем функцию int() и уже к этому значению прибавляем 1
    
    sorted() нам не подходит, если туннелей больше 10. Поэтому используем natsort.natsorted()
    '''
    regex = r'Tunnel(\d+).*'
    list_of_tunnel_interfaces_on_both = natsort.natsorted(re.findall(regex, local_sh_ip_int_br + remote_sh_ip_int_br))

    return int(list_of_tunnel_interfaces_on_both[-1]) + 1

if __name__ == "__main__":
    r1 = {'device_type': 'cisco_ios',
      'host': '192.168.100.1',
      'username': 'cisco',
      'password': 'cisco',
      'secret': 'cisco'
    }

    r2 = {'device_type': 'cisco_ios',
      'host': '192.168.100.2',
      'username': 'cisco',
      'password': 'cisco',
      'secret': 'cisco'
    }

    template1_file = "templates/gre_ipsec_vpn_1.txt"
    template2_file = "templates/gre_ipsec_vpn_2.txt"
    
    pprint(configure_vpn(r1, r2, template1_file, template2_file, data))
