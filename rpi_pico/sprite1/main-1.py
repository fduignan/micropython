from machine import Pin, Timer,SPI, PWM
import urandom
import time
import st7735
import sprite
import sprites
import controller
display=st7735.st7735()
display.clear()
#print(display.write_block(2,3,4))
dpad=controller.controller()
display.clear()
urandom.seed()
display.setOrientation(0,1)
deco=sprite.sprite(0,0,12,16,sprites.sprite1,display)
deco.show()
x = 0
y = 0
moved = 0
count=0
colour=0
start=time.time()
while(count < 1000):
    count = count + 1
    display.fillRectangle(0,0,50,50,colour)
    colour=colour+1
print(time.time()-start)
while(1):
    x1=urandom.randint(0,120)
    y1=urandom.randint(0,150)
    x2=urandom.randint(0,120)
    y2=urandom.randint(0,150)
    w=urandom.randint(1,127-x1)
    h=urandom.randint(1,159-y1)
    colour=urandom.randint(0,65535)    
    display.drawCircle(x1,y1,x2,colour)
    #display.drawRectangle(x1,y1,w,h,colour)
    #if (dpad.rightPressed()):
    #    if (x < display.screen_width-deco.width):
    #        deco.setOrientation(1,1)
    #        x=x+1
    #        moved = 1
    #if (dpad.leftPressed()):
    #    if (x > 0):
    #        deco.setOrientation(0,1)        
    #        x=x-1
    #        moved = 1
    #if (dpad.upPressed()):
    #    if (y > 0):            
    #        y=y-1
    #        moved = 1
    #if (dpad.downPressed()):
    #    if (y < display.screen_height-deco.height):                
     #       y=y+1
     #       moved = 1                        
    #if (moved == 1):
     #   deco.move(x,y)
     #   moved = 0
    #display.print(str(x),0,0,display.RGBToWord(0,0xff,0xff),0)

    

