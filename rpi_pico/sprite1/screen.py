from machine import Pin, Timer,SPI
import time
class st7735:
    def __init__(self):        
        # configure pins for output
        self.reset=Pin(21,Pin.OUT)
        self.cs=Pin(22,Pin.OUT)
        self.a0=Pin(20,Pin.OUT)
        self.spi=SPI(0,baudrate=1000000,polarity=1,phase=1,bits=8,firstbit=machine.SPI.MSB,sck=machine.Pin(18),mosi=machine.Pin(19))        
        self.cs.value(1)
        self.reset.value(1)
        time.sleep_ms(10)
        
        self.reset.value(0)
        time.sleep_ms(200)
        
        self.reset.value(1)
        time.sleep_ms(200)
        self.cs.value(200)
        time.sleep_ms(200)
        
        self.cs.value(0)
        time.sleep_ms(20)
        
        self.command(1) # software reset
        time.sleep_ms(100)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0x11)
        time.sleep_ms(120)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)        
        time.sleep_ms(1)
        
        self.command(0xb1)
        self.data(0x05)
        self.data(0x3c)
        self.data(0x3c);
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0xb2)
        self.data(0x05)
        self.data(0x3c)
        self.data(0x3c);        
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0xb3)
        self.data(0x05)
        self.data(0x3c)
        self.data(0x3c)
        self.data(0x05)
        self.data(0x3c)
        self.data(0x3c)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0xb4)
        self.data(0x03)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0x36)
        self.data(0xc8)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0x3a)
        self.data(0x05)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0x29)
        time.sleep_ms(100)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0x2c)        
        self.fillRectangle(0,0,128,160,0xffff)
        
    def command(self,cmd):
        self.a0.value(0)
        msg=bytearray()
        msg.append(cmd)
        self.spi.write(msg)
        
    def data(self,cmd):
        self.a0.value(1)
        msg=bytearray()
        msg.append(cmd)
        self.spi.write(msg)        
    def openAperture(self,x1,x2,y1,y2):
        self.command(0x2a)
        self.data(x1 >> 8)
        self.data(x1 & 0xff)
        self.data(x2 >> 8)
        self.data(x2 & 0xff)
        self.command(0x2b)
        self.data(y1 >> 8)
        self.data(y1 & 0xff)
        self.data(y2 >> 8)
        self.data(y2 & 0xff)        
        self.command(0x2c)
    def fillRectangle(self,x1,y1,w,h,colour):
        self.openAperture(x1,x1+w-1,y1,y1+h-1)
        self.a0.value(1)
        pixelcount=h*w
        msg=bytearray()
        while(pixelcount >0):
            pixelcount = pixelcount-1
            msg.append(colour >> 8)
            msg.append(colour & 0xff)
        self.command(0x2c)
        self.spi.write(msg)
            
display=st7735()
led=Pin(25,Pin.OUT)
tim=Timer()
def tick(timer):
    global led
    led.toggle()    
tim.init(freq=1,mode=Timer.PERIODIC,callback=tick)
