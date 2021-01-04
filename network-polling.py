# Python script to poll network devices for status
# Version 2.0.0 - net.gini@gmail.com

from netmiko import ConnectHandler

nw_device_ip = '192.168.255.249'
nw_device_username = 'cisco'
nw_device_password = 'cisco'

device = ConnectHandler(device_type='cisco_ios', ip='192.168.255.249', username=nw_device_username, password=nw_device_password)
output = device.send_command("show version")
print (output)
device.disconnect()