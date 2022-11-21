from machine import Pin, Timer,SPI
import time
class controller:
    def __init__(self):
        self.left=Pin(14,Pin.IN, Pin.PULL_UP)
        self.right=Pin(12,Pin.IN, Pin.PULL_UP)
        self.up=Pin(15,Pin.IN, Pin.PULL_UP)
        self.down=Pin(13,Pin.IN, Pin.PULL_UP)
    def leftPressed(self):
        if (self.left.value()==0):
            return 1
        else:
            return 0
    def rightPressed(self):
        if (self.right.value()==0):
            return 1
        else:
            return 0
    def upPressed(self):
        if (self.up.value()==0):
            return 1
        else:
            return 0
        
    def downPressed(self):
        if (self.down.value()==0):
            return 1
        else:
            return 0
        
        
