import obd
import time
import msvcrt

ports = obd.scan_serial()

connection = obd.OBD(portstr=ports, baudrate=19200, fast=False)
while not connection.is_connected():
    time.sleep(0.5)
print("CONNECTED")

while not msvcrt.kbhit():
    rSpeed = connection.query(obd.commands.SPEED)  # send the command, and parse the response
    print(rSpeed.value) # returns unit-bearing values thanks to Pint
    print(rSpeed.value.to("mph"))
