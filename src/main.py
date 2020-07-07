from random import randint
from machine import UART, Pin, DAC, deepsleep
from utime import sleep, ticks_ms
import struct
#from math import cos, pi
from esp32 import wake_on_ext1
from MicroWebSrv2 import MicroWebSrv2
import urequests

print("Your public IP address is: ", urequests.get('https://api.ipify.org').text)

uart = UART(1, 115200)
uart.init(115200, bits=8, parity=None, stop=1, tx=15, rx=2)

dac=DAC(Pin(25))

#dist_list=[]
#strength_list=[]
#cycle=True

red = Pin(21, Pin.OUT)
yellow = Pin(22, Pin.OUT)
green = Pin(19, Pin.OUT)
leds = Pin(23, Pin.IN, Pin.PULL_UP)
nap = Pin(18, Pin.IN, Pin.PULL_UP)
wake = Pin(4, mode = Pin.IN, pull = Pin.PULL_DOWN)
wake_on_ext1(pins = [wake], level = Pin.WAKE_HIGH)

# pylint: disable=global-statement, unused-argument
myWebSockets = None
def OnWebSocketTextMsg(webSocket, msg):
    print('Received message: {0}'.format(msg))
    red.value(True if msg == "RED LED ON" else False)
def OnWebSocketClosed(webSocket):
    global myWebSockets
    myWebSockets = None
def OnWebSocketAccepted(microWebSrv2, webSocket):
    global myWebSockets
    if myWebSockets is None:
        print('WebSocket from {0}'.format(webSocket.Request.UserAddress))
        myWebSockets = webSocket
        myWebSockets.OnTextMessage = OnWebSocketTextMsg
        myWebSockets.OnClosed = OnWebSocketClosed

mws2 = MicroWebSrv2()
wsMod = MicroWebSrv2.LoadModule('WebSockets')
wsMod.OnWebSocketAccepted = OnWebSocketAccepted
mws2.SetEmbeddedConfig()
mws2.NotFoundURL = '/'
mws2.StartManaged()

c=0
try:
    while mws2.IsRunning:
        # deepsleep button
        if nap.value()==False:
            print("Going to sleep...")
            sleep(1)
            print("zzz")
            deepsleep()
    
        x = uart.read(1)
        if not x or x[0] != 0x59:
            continue
        #print(x,0x59,type(x),type(0x59))
        data = uart.read(8)
        #print(data)
        frame, dist, strength, mode, _, checksum = struct.unpack("<BHHBBB", data)
        # look for second 0x59 frame indicator
        if frame != 0x59:
            continue
        # calculate and check sum
        mysum = (sum(data[0:7]) + 0x59) & 0xFF
        if mysum != checksum:
            continue

        c+=1
        if c%100==0:
            print('Distance: ',dist)
            print('Strength: ',strength)
            
            if dist<801:
                d = open('www/dist.txt','w')
                d.write(str(dist).encode('ascii'))
                d.close()

                s = open('www/strength.txt','w')
                s.write(str(strength).encode('ascii'))
                s.close()

        # leds for signal strength
        red.value(False)
        yellow.value(False)
        green.value(False)
        if leds.value()==False:
            print(strength)
            if strength<50:
                red.value(True)
            elif strength<150:
                yellow.value(True)
            else:
                green.value(True)
                
        # play an entire cycle
        # if cycle==True:
        #     print(dist)
        #     freq=583/(2**(min(dist,800)/192.5))
        #     print(max(dist,800))
        #     print(freq)
        #     Tms=1000/freq
        #     t0=ticks_ms()
        #     cycle=False
        # t=ticks_ms()-t0
        # dac.write(int(127.5+127.5*cos(2*pi*freq*t)))
        # if t>Tms:
        #     cycle=True

except KeyboardInterrupt:
    pass
red.value(False)
yellow.value(False)
green.value(False)
mws2.Stop()
