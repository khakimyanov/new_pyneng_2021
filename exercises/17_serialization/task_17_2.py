# -*- coding: utf-8 -*-
"""
Задание 17.2

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений
  и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv),
   в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена
  информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы (именно в этом порядке):
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается
на sh_vers. Вы можете раскомментировать строку print(sh_version_files),
чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""
import re
import csv
import glob
from pprint import pprint

sh_version_files = glob.glob("sh_vers*")
#print(sh_version_files)

headers = ["hostname", "ios", "image", "uptime"]


def parse_sh_version(sh_ver_input):
    regex = (r'Cisco IOS Software, .+, Version (\S+),.+'
             r'|System image file is "(.+)"'
             r'|router uptime is (.+)')
    
    for row in sh_ver_input.split('\n'):
        match = re.search(regex, row)
        if match and match.lastindex == 1:
            ios = match.group(1)
        elif match and match.lastindex == 2:
            image = match.group(2)
        elif match and match.lastindex == 3:
            uptime = match.group(3)

    return ios, image, uptime

    
def write_inventory_to_csv(data_filenames, csv_filename):
    result = []
    result.append(headers)
    
    for file in data_filenames:
        hostname = file.split('.')[0].split('_')[-1]
        with open(file, 'r') as f:
            result.append([hostname] + list(parse_sh_version(f.read())))
    
    with open(csv_filename, 'w') as dst:
        writer = csv.writer(dst, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(result)

if __name__ == "__main__":
    write_inventory_to_csv(sh_version_files, 'routers_inventory.csv')

"""
И опять, нужно было сначала открыть csv файл на запись, и уже потом
обрабатывать sh version файлы, сразу записывая данные в csv файл, без 
необходимости создавать дополнительный контейнер result

Наталья в свою очередь предлагает оптимизировать функцию
def parse_sh_version(sh_ver_input):
    regex = (r'Cisco IOS Software, .+, Version (?P<ios>\S+),.+'
             r'System image file is "(?P<image>.+)"'
             r'router uptime is (?P<uptime>.+)')
    match = re.search(regex, sh_ver_input)
    if match:
        return match.group("ios", "image", "uptime")

Как мы видим, regex идет как единое целое, я же в своем решении 
использовал оператор "|", поэтому у меня было совпадение по одному
элементу, а не по всему выражению.

"""
