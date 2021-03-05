# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

"""
import re
from netmiko.cisco.cisco_ios import CiscoIosSSH


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании, возникла ошибка.
    """


class MyNetmiko(CiscoIosSSH):
    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.enable()
    
    def send_command(self, command):
        output = super().send_command(command)
        if not self._check_error_in_command(command, output):
            return output
    
    def send_config_set(self, commands):
        result = ''
        
        if type(commands) == str:
            commands = [commands]
            
        for command in commands:
            output = super().send_config_set(command)
            if not self._check_error_in_command(command, output):
                result += output
        
        return result
            
    def _check_error_in_command(self, command, command_output):
        regex = r'% (.*)(?:\n)*'
        match = re.search(regex, command_output)
        if match:
            raise ErrorInCommand(f'При выполнении команды "{command}" на устройстве {self.host} возникла ошибка "{match.group(1)}"')
