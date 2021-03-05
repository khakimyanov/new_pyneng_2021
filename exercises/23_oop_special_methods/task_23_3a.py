# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
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
        self._index = 0  
        
    def __add__(self, other):
        common_topology = self.topology.copy()
        common_topology.update(other.topology)
        
        return Topology(common_topology)
    
    def __next__(self):
        print('__next__ working...')
        if self._index < len(self.topology):
            current_item = tuple(self.topology.items())[self._index]
            self._index += 1
            return current_item
        else:
            self._index = 0
            raise StopIteration
        
    def __iter__(self):
        print('__iter__ working...')
        return iter(self.topology.items())
    
    def __getitem__(self, index):
        print('__getitem__ working...')
        if index < len(self.topology):
            return tuple(self.topology.items())[index]
            
        else:
            raise IndexError
           
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
        non_exist = True
        
        for local_link, remote_link in self.topology.copy().items():
            if node_to_delete in local_link or node_to_delete in remote_link:
                del self.topology[local_link]
                non_exist = False
        if non_exist:
            print("Такого устройства нет")
