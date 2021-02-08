# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""
from task_12_1 import ping_ip_addresses
from tabulate import tabulate

def print_ip_table(reachable_ips, unreachable_ips):
    ip_dict = {}
    ip_dict['Reachable'] = reachable_ips
    ip_dict['Unreachable'] = unreachable_ips
    print(tabulate(ip_dict, headers = 'keys', tablefmt = "markdown"))


if __name__ == "__main__":
    ip_list = ['8.8.8.8', '80.255.128.1', 'a', '10.1.1.1']
    #print(ping_ip_addresses(ip_list))
    print_ip_table(*ping_ip_addresses(ip_list))

"""
Натальино решение как обычно более короткое
def print_ip_table(reach_ip, unreach_ip):
   table = {"Reachable": reach_ip, "Unreahable": unreach_ip}
   print(tabulate(table, headers = keys))
"""
