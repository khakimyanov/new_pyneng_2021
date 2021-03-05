# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


"""

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
           
    def _normalize(self, full_topology):
        clean_topology = {}
        
        for local_link, remote_link in full_topology.items():
            if clean_topology.get(remote_link) != local_link:
                clean_topology[local_link] = remote_link        
        
        return clean_topology
    
    def delete_link(self, local_link, remote_link):
        if self.topology.get(local_link) and self.topology[local_link] == remote_link:
            del self.topology[local_link]
        elif self.topology.get(remote_link) and self.topology[remote_link] == local_link:
            del self.topology[remote_link]
        else:
            print("Такого соединения нет")
    
    def delete_node(self, node_to_delete):
        not_exist = True
        
        for local_link, remote_link in self.topology.copy().items():
            if node_to_delete in local_link or node_to_delete in remote_link:
                del self.topology[local_link]
                not_exist = False
        if not_exist:
            print("Такого устройства нет")
            
    def add_link(self, local_link, remote_link):
        if self._check_connection_exist(local_link, remote_link):
            print(self._link_exist_message)
        else:
            self.topology[local_link] = remote_link
    
    def _check_connection_exist(self, local_link, remote_link):
        self._link_exist_message = 'Cоединение с одним из портов существует'
        
        #Сначала проверяем нет ли совпадений вида:
        # - значение совпадает, но не совпадает ключ.
        for link in self.topology:
            first_value = (link != local_link and self.topology[link] == remote_link)
            second_value = (link != remote_link and self.topology[link] == local_link)
            
            if any([first_value, second_value]):
                return True
        
        #теперь проверяем именно ключи и возможное полное совпадение
        if self.topology.get(local_link):
            if self.topology[local_link] == remote_link:
                self._link_exist_message = 'Такое соединение существует'
            return True
        elif self.topology.get(remote_link):
            if self.topology[remote_link] == local_link:
                self._link_exist_message = 'Такое соединение существует'
            return True
        else:
            return False

"""
Натальино решение 
    def add_link(self, src, dest):
        keys_and_values = self.topology.keys() | self.topology.values()
        if self.topology.get(src) == dest:
            print("Такое соединение существует")
        elif src in keys_and_values or dest in keys_and_values:
            print("Cоединение с одним из портов существует")
        else:
            self.topology[src] = dest
"""
