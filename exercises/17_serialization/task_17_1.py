# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает вывод
команды show dhcp snooping binding из разных файлов и записывает обработанные
данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

Первый столбец в csv файле имя коммутатора надо получить из имени файла,
остальные - из содержимого в файлах.

Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt,
sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.

"""
import re
import csv
dhcp_snooping_files = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']


def write_dhcp_snooping_to_csv(filenames, output):
    result = []
    headers = ['switch', 'mac', 'ip', 'vlan', 'interface']
    result.append(headers)
    regex = r'(\S+) +(\S+) +(?:\d+) +(?:\S+) +(\d+) +(\S+)'
    for file in filenames:
        with open(file, 'r') as src:
            device = file.split('_')[0]
            for line in src:
                match = re.search(regex, line)
                if match:
                    mac,ip,vlan,interface = match.groups()
                    result.append([device, mac,ip,vlan,interface])
    
    with open(output, 'w') as dst:
        writer = csv.writer(dst)
        for row in result:
            writer.writerow(row)

if __name__ == "__main__":
    write_dhcp_snooping_to_csv(dhcp_snooping_files, 'dhcp_snooping_data.csv')

"""
Как всегда избыточность в решении. В прошлый раз я сделал более элегатно - сначала
открыл scv файл на запись, а уже потом по мере обработки файлов записывал построчно
в csv файл

def write_dhcp_snooping_to_csv(filenames, output):
    headers = ['switch', 'mac', 'ip', 'vlan', 'interface']
    regex = r'(\S+) +(\S+) +(?:\d+) +(?:\S+) +(\d+) +(\S+)'
    
    with open(path + output, 'w') as dst:
        writer = csv.writer(dst)
        writer.writerow(headers)
        
        for file in filenames:
            with open(path+file, 'r') as src:
                device = file.split('_')[0]
                for line in src:
                    match = re.search(regex, line)
                    if match:
                        writer.writerow([device] + list(match.groups())
"""
