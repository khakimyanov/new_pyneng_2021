# -*- coding: utf-8 -*-
"""
Задание 11.2

Создать функцию create_network_map, которая обрабатывает
вывод команды show cdp neighbors из нескольких файлов и объединяет его в одну
общую топологию.

У функции должен быть один параметр filenames, который ожидает как аргумент
список с именами файлов, в которых находится вывод команды show cdp neighbors.

Функция должна возвращать словарь, который описывает соединения между
устройствами. Структура словаря такая же, как в задании 11.1:
    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}


Cгенерировать топологию, которая соответствует выводу из файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt

Не копировать код функций parse_cdp_neighbors и draw_topology.
Если функция parse_cdp_neighbors не может обработать вывод одного из файлов
с выводом команды, надо исправить код функции в задании 11.1.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
infiles = [
    "sh_cdp_n_sw1.txt",
    "sh_cdp_n_r1.txt",
    "sh_cdp_n_r2.txt",
    "sh_cdp_n_r3.txt",
]
#старое решение
from pprint import pprint
from draw_network_graph import draw_topology 

path = "/home/python/github/khakimyanov-9/exercises/11_modules/"

# эти заготовки написаны чтобы показать в какой момент должна
# рисоваться топология (после вызова функции)
def create_network_map(filenames):
    sh_cdp_neigbors = {}
    for file in filenames:
        with open(path + file, 'r') as f:
            for line in f:
                if 'show cdp neighbors' in line:
                    device = line.split('>')[0]
                elif line.strip() and '/' in line.split()[-1]:
                    remote, local_intf, local_port, *other, remote_intf, remote_port = line.split()
                    sh_cdp_neigbors[(device, local_intf + local_port)] = (remote, remote_intf + remote_port) 
    
    for key in sh_cdp_neigbors.keys():
        for value in sh_cdp_neigbors.values():
            if key == value:
                sh_cdp_neigbors[key] = None
    for key in sh_cdp_neigbors.copy():
        if sh_cdp_neigbors[key] == None:
            del sh_cdp_neigbors[key]

    return sh_cdp_neigbors

if __name__ == "__main__":
    infiles = [
        "sh_cdp_n_sw1.txt",
        "sh_cdp_n_r1.txt",
        "sh_cdp_n_r2.txt",
        "sh_cdp_n_r3.txt",
    ]

    topology = create_network_map(infiles)
    #pprint(topology)
    # рисуем топологию:
    draw_topology(topology)

"""
Натальино решение намного короче и элегантнее
Во первый она импортирует уже готовую функцию из task_11_1
from task_11_1 import parsed_cdp_neighbors

def create_network_map(filenames):
    network_map = {}
    for filename in filenames:
        with open(filename, 'r') as show_command:
            parsed = parse_cdp_neighbors(show_command.read())
            for key, value in parsed.items():
                if not network_map.get(value) == key:
                    network_map[key] = value
    return network_map

Еще один вариант

def create_network_map(filenames):
    network_map = {}
    
    for filename in filenames:
        with open(filename, 'r') as show_command:
            parsed = parse_cdp_neighbors(show_command.read())
            for key, value in parsed.items():
                key, value = sorted([key, value])
                network_map[key] = value
    return network_map
"""
