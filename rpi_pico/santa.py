import st7735
import sprite
import sprites
import controller
import time
import sound
class santa:
    def __init__(self,display,controller,snd):
        self.controller = controller
        self.display = display
        self.snd=snd
        self.hit = 0
        self.miss = 0
        self.santa=sprite.sprite(0,0,11,18,sprites.santa1_sprite,display)
        self.gift=sprite.sprite(40,40,5,8,sprites.gift_sprite,display)
        self.chimney=sprite.sprite(114,110,14,17,sprites.chimney1_sprite,display)
        self.helicopter1=sprite.sprite(100,50,18,11,sprites.helicopter1_sprite,display)
        self.helicopter2=sprite.sprite(100,50,18,11,sprites.helicopter2_sprite,display)
        self.jinglebells=[sound.note(self.snd.E4,100,100),sound.note(self.snd.E4,100,100),sound.note(self.snd.E4,100,200),sound.note(self.snd.E4,100,100),sound.note(self.snd.E4,200,100),sound.note(self.snd.E4,100,100),
        sound.note(self.snd.G5,100,100),sound.note(self.snd.C4,100,100),sound.note(self.snd.D4,100,100),sound.note(self.snd.E4,100,100),
        sound.note(self.snd.F4,100,100),sound.note(self.snd.F4,100,100),sound.note(self.snd.F4,100,100),sound.note(self.snd.F4,100,100),sound.note(self.snd.E4,100,100),
        sound.note(self.snd.E4,100,100),sound.note(self.snd.E4,100,100),sound.note(self.snd.E4,100,100),sound.note(self.snd.E4,100,100),
        sound.note(self.snd.D4,100,100),sound.note(self.snd.D4,100,100),sound.note(self.snd.E4,100,100),sound.note(self.snd.D4,100,100),sound.note(self.snd.G5,100,200),
        sound.note(self.snd.E4,100,100),sound.note(self.snd.E4,100,100),sound.note(self.snd.E4,100,200),sound.note(self.snd.E4,100,100),sound.note(self.snd.E4,200,100),sound.note(self.snd.E4,100,100),
        sound.note(self.snd.G5,100,100),sound.note(self.snd.C4,100,100),sound.note(self.snd.D4,100,100),sound.note(self.snd.E4,100,100),
        sound.note(self.snd.F4,100,100),sound.note(self.snd.F4,100,100),sound.note(self.snd.F4,100,100),sound.note(self.snd.F4,100,100),sound.note(self.snd.E4,100,100),
        sound.note(self.snd.E4,100,100),sound.note(self.snd.E4,100,100),sound.note(self.snd.E4,100,100),sound.note(self.snd.E4,100,100),
        sound.note(self.snd.G5,100,100),sound.note(self.snd.G5,100,100),sound.note(self.snd.F4,100,100),sound.note(self.snd.D4,100,100),sound.note(self.snd.C4,100,100)]

    def play(self):
        self.display.clear()
        self.chimney.show()
        self.santa.show()
        self.snd.tune=self.jinglebells
        self.display.drawLine(0,127,127,127,self.display.RGBToWord(0xff,0xff,0))
        self.showScores()
        x = 0 # current x position for santa
        y = 0 # y position for santa
        moved = 0 # did santa move?
        chimney_x=114 # initial location for a chimney
        start_time=time.ticks_ms() # note current time (used to pace the game)
        helicopter_image=1
        h_x = self.helicopter1.x
        h_y = self.helicopter1.y
        v_h_x = 1
        while(1):
            if ((time.ticks_ms()-start_time) > 20): # has 20ms passed?
                chimney_x = chimney_x - 1 # if so the move the chimney
                start_time=time.ticks_ms() # note the current time
                h_x = h_x + v_h_x
                if (h_x > 109):
                    v_h_x = -1
                if (h_x < 2):
                    v_h_x = 1
                
                if (helicopter_image==1):
                   # self.helicopter1.hide()
                    self.helicopter2.move_no_erase(h_x,h_y)
                    self.helicopter2.show()
                    helicopter_image=2
                if (helicopter_image==2):
                    self.helicopter1.move_no_erase(h_x,h_y)
                    self.helicopter1.show()
                  #  self.helicopter2.hide()
                    helicopter_image=1
            # update chimney position 
            if (chimney_x > 0): 
                self.chimney.move_no_erase(chimney_x,self.chimney.y)
            else:
                chimney_x=114
                self.chimney.move(chimney_x,self.chimney.y)
                
            # move the gift downwards if it is visible
            if (self.gift.visible==1):
                self.gift.move_no_erase(self.gift.x,self.gift.y+1)
                if (self.gift.y > 110):
                    self.gift.hide()
                    if (self.gift.x > self.chimney.x) and (self.gift.x+self.gift.width < self.chimney.x+self.chimney.width):
                        self.hit=self.hit+1
                    else:
                        self.miss=self.miss+1
                    self.showScores()
            # figure out where santa is and see if the proposed move is allowed
            proposed_x = x
            proposed_y = y
            if (self.controller.rightPressed()):
                if (x < self.display.screen_width-self.santa.width):
                    self.santa.setOrientation(1,1)
                    proposed_x=x+1
                    moved = 1
            if (self.controller.leftPressed()):
                if (x > 0):
                    self.santa.setOrientation(0,1)        
                    proposed_x=x-1
                    moved = 1
            if (self.controller.upPressed()):
                if (y > 0): 
                    proposed_y=y-1
                    moved = 1
            if (self.controller.downPressed()):
                if (y < 127 - self.santa.height):                
                   proposed_y=y+1
                   moved = 1
            if (self.controller.aPressed()):
                if (self.gift.visible==0):
                    self.gift.move(x,y+self.santa.height)
                    self.gift.show()
            if (self.controller.bPressed()):
                return
            if (moved == 1):
                # try out the new position
                self.santa.x=proposed_x
                self.santa.y=proposed_y
                # check to see if we have run into anything
                if (self.santa.isOverlapping(self.chimney)==0):
                    # if not then update santa on screen
                    self.santa.x=x
                    self.santa.y=y
                    x=proposed_x
                    y=proposed_y                    
                    self.santa.move_no_erase(x,y)
            if (self.helicopter1.isOverlapping(self.santa)==1):
                for i in range(1,10):
                    self.display.fillCircle(self.santa.x,self.santa.y,30,self.display.RGBToWord(255,0,0))
                    self.display.fillCircle(self.santa.x,self.santa.y,30,self.display.RGBToWord(255,255,255))
                return
            if (self.helicopter2.isOverlapping(self.santa)==1):
                for i in range(1,10):
                    self.display.fillCircle(self.santa.x,self.santa.y,30,self.display.RGBToWord(255,0,0))
                    self.display.fillCircle(self.santa.x,self.santa.y,30,self.display.RGBToWord(255,255,255))
                return
            if (self.helicopter1.isOverlapping(self.gift)==1):
                if (self.gift.visible==1):
                    self.gift.hide()
                    self.miss = self.miss + 1
                    print("Gift shredded")
                    self.showScores()

            if (self.helicopter2.isOverlapping(self.gift)==1):
                if (self.gift.visible==1):
                    self.gift.hide()
                    self.miss = self.miss + 1
                    print("Gift shredded")
                    self.showScores()

                moved = 0    
    def showScores(self):
        self.display.print("Hit",0,128,self.display.RGBToWord(0xf,0xf,0xff),0)
        self.display.fillRectangle(18,128,46,8,0)
        self.display.print(str(self.hit),22,128,self.display.RGBToWord(0xf,0xf,0xff),0)
        self.display.print("Miss",64,128,self.display.RGBToWord(0xff,0xf,0xf),0)
        self.display.fillRectangle(82,128,45,8,0)
        self.display.print(str(self.miss),94,128,self.display.RGBToWord(0xff,0xf,0xf),0)