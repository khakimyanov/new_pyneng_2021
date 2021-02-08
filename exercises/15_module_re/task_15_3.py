# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""
import re

template = ('object network LOCAL_{0}\n'
            ' host {0}\n'
            ' nat (inside,outside) static interface service {1} {2} {3}\n')

def convert_ios_nat_to_asa(ios_nat_file, asa_nat_file):
    regex = r"ip nat inside source static (\S+) (\S+) (\S+) interface (?:\S+) (\S+)"
    
    with open(ios_nat_file, 'r') as src, open(asa_nat_file, 'w') as dst:
        for line in src:
            match = re.search(regex, line)
            if match:
                proto, ipaddr, src_port, dst_port = match.groups()
                dst.write(template.format(ipaddr, proto, src_port, dst_port))
    
    
if __name__ == "__main__":
    convert_ios_nat_to_asa("cisco_nat_config.txt", "asa_nat_config.txt")

"""
Натальино решение
def convert_ios_nat_to_asa(cisco_ios, cisco_asa):
    regex = (
        "tcp (?P<local_ip>\S+) +(?P<lport>\d+) +interface +\S+ (?P<outside_port>\d+)"
    )
    asa_template = (
        "object network LOCAL_{local_ip}\n"
        " host {local_ip}\n"
        " nat (inside,outside) static interface service tcp {lport} {outside_port}\n"
    )
    with open(cisco_ios) as f, open(cisco_asa, "w") as asa_nat_cfg:
        data = re.finditer(regex, f.read())
        for match in data:
            asa_nat_cfg.write(asa_template.format(**match.groupdict()))


if __name__ == "__main__":
    convert_ios_nat_to_asa("cisco_nat_config.txt", "cisco_asa_config.txt")
"""
