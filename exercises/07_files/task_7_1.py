# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
template = ('Prefix                {}\n'
            'AD/Metric             {}\n'
            'Next-Hop              {}\n'
            'Last update           {}\n'
            'Outbound Interface    {}\n'
)

with open('ospf.txt', 'r') as f:
	for line in f:
		_, ip, ad, _, nhop, last_update, intf = line.replace('[', '').replace(']', '').replace(',', '').split()
		print(template.format(ip, ad, nhop, last_update, intf), end='')
