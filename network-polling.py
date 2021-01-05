# Python script to poll network devices for status
# Gineesh - net.gini@gmail.com
from datetime import datetime
from netmiko import ConnectHandler

nw_device_ip = '192.168.1.10'
nw_device_username = 'cisco'
nw_device_password = 'cisco'
nw_device_type = 'cisco_ios'

nw_commands_run = {
  "ter len 0",
  "show ver | in uptime",
  "show sdwan version",
  "show platform resources",
  "show process memory sorted",
  "show processes memory platform sorted",
  "show platform software status control-processor",
  "show platform software process list 0 summary",
  "show platform software process list RP active sort memory",
  "show platform software process slot RP active monitor cycles",
  "show platform software process memory r0 all sorted"
}

dateTimeObj = datetime.now()
daeTimeString = dateTimeObj.strftime("%d-%b-%Y_%H-%M-%S_%f")
log_filename = "log" + daeTimeString + ".txt"

# initiate file line with date
log_file = open(log_filename, "w")
log_file.write( "\n" + daeTimeString + ": Device Log")
log_file.close()

device = ConnectHandler(device_type=nw_device_type, ip=nw_device_ip, username=nw_device_username, password=nw_device_password)

# execute each command and append output to log file
for nw_command in nw_commands_run:
  #print(nw_command)
  command_output = device.send_command(nw_command)
  log_file = open(log_filename, "a")
  log_file.write( "\n" + command_output )
  log_file.close()

#close connection
device.disconnect()

print("\n\nLogs are stored in : " + log_filename)
