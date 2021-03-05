# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""
import telnetlib
import time
from textfsm import clitable


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret

        self._telnet = telnetlib.Telnet(ip)
        self._telnet.read_until(b"Username")
        self._write_line(username)
        self._telnet.read_until(b"Password")
        self._write_line(password)
        
        self._write_line("enable")
        self._telnet.read_until(b"Password")
        self._write_line(secret)
        self._telnet.read_until(b"#", timeout=5)
        self._write_line("terminal length 0")
        self._telnet.read_until(b"#", timeout=5)
        time.sleep(3)
        self._telnet.read_very_eager()

    def send_show_command(self, command, parse=True, templates='templates', index='index'):
        self._write_line(command)
        output = self._telnet.read_until(b"#", timeout=5).decode('utf-8')
        
        if parse:
            cli_table = clitable.CliTable(index, templates)
            attributes = {'Command': command, 'Vendor': 'cisco_ios'}
            cli_table.ParseCmd(output, attributes)
            
            headers = list(cli_table.header)
            return [dict(zip(headers, row)) for row in cli_table]
        else:
            return output
    
    def send_config_commands(self, commands):
        if type(commands) == str:
            commands = [commands]
        
        #open conf-mode:
        self._write_line('conf t')
        
        for command in commands:
            self._write_line(command)
            time.sleep(0.5)
                
        #close conf-mode
        self._write_line('end')
        time.sleep(2)
        output = self._telnet.read_very_eager()
        
        return output.decode('utf-8')
        
    def _write_line(self, line):
        return self._telnet.write(line.encode("ascii") + b"\n")
"""
Наталья так же напоминает что можно сделать проверку таким образом
if isinstance(commands, str):
    commands = [commands]

К тому же я сделал процесс захода в конфигурационных режим и выхода из
него отдельными строчками внутри функции. Наталья же предлагает более
красивый вариант
    def send_config_commands(self, commands):
        if isinstance(commands, str):
            commands = [commands]
        commands = ["conf t", *commands, "end"]
        for command in commands:
            self._write_line(command)
            time.sleep(1)
        return self.telnet.read_very_eager().decode("ascii")

"""
