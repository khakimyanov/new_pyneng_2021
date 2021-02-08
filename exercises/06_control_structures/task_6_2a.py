# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
ip = input("Введите IP-адрес: ").split('.')

if not len(ip) == 4 or not all([item.isdigit() for item in ip]) or not all([int(item) in range(0, 256) for item in ip]):
    print("Неправильный IP-адрес")
elif int(ip[0]) in range(1, 224):
    print("unicast")
elif int(ip[0]) in range(224, 240):
    print("multicast")
elif ip == ['255', '255', '255', '255']:
    print("local broadcast")
elif ip == ['0','0','0','0']:
    print("unassigned")
else:
    print("unused")

'''
Решение от Натальи
ip = input("Введите IP-адрес в формате x.x.x.x: ")
octets = ip.split(".")

#Вводитя параметр проверки является ли IP-адрес верным
valid_ip = len(octets) == 4

for i in octets:
    valid_ip = i.isdigit() and 0 <= int(i) <=255 and valid_ip

if valid_ip:
    if int(ip[0]) in range(1, 224):
        print("unicast")
    elif int(ip[0]) in range(224, 240):
        print("multicast")
    elif ip == ['255', '255', '255', '255']:
        print("local broadcast")
    elif ip == ['0','0','0','0']:
        print("unassigned")
    else:
        print("unused")
'''
"""
Еще немного от Натальи

ip_address = input("Enter ip address: ")
octets = ip_address.split(".")
correct_ip = True

if len(octets) != 4:
    correct_ip = False
else:
    for octet in octets:
        # тут второе условие int(octet) in range(256)
        # проверяется только в том случае, если первое условие истина
        # Если встретился хоть один октет с нарушением,
        # дальше можно не смотреть
        if not (octet.isdigit() and int(octet) in range(256)):
            correct_ip = False
            break

if not correct_ip:
    print("Неправильный IP-адрес")
else:
    octets_num = [int(i) for i in octets]

    if octets_num[0] in range(1, 224):
        print("unicast")
    elif octets_num[0] in range(224, 240):
        print("multicast")
    elif ip_address == "255.255.255.255":
        print("local broadcast")
    elif ip_address == "0.0.0.0":
        print("unassigned")
    else:
        print("unused")
"""
