from network import WLAN
from machine import I2C
import bme280
import socket

wlan = WLAN()
wlan.init( mode= wlan.AP, ssid= 'Teste01', auth=(wlan.WPA2, 'nelio'))

i2c = I2C(0, I2C.MASTER, baudrate=100000)
bme = bme280.BME280(i2c=i2c)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    
    dados = bme.formated_values

    html  = "<!DOCTYPE html>"
    html += "<head>"
    html += "    <meta http-equiv='refresh' content='2'>"
    html += "</head>"
    html += "<body>"
    html += dados
    html += "</body></html>"

    cl.send(html)
    cl.close()
