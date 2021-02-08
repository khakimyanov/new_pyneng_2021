# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
from sys import argv
ignore = ["duplex", "alias", "Current configuration"]
path = '/home/python/github/khakimyanov-9/exercises/07_files/'

filename = argv[1]

with open(path + filename, 'r') as f:
	for line in f:
		if not line.startswith('!') and all([word not in line for word in ignore]):
			print(line.rstrip())
