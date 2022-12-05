import st7735
import sprite
import sprites
import controller
import time
import random
import sound
class brici:
    
    def __init__(self,display,controller,snd):
        # This is the constructor for the brici game.
        # it is called when the brici game object is created.
        # The code that creates this game must pass a reference
        # to the display device and the controller
        self.controller = controller # store reference to controller within this object
        self.display = display # store reference to the display within this object
        self.snd=snd # store reference to sound output object
        random.seed() # initialize the random numeber generator so the game doesn't repeat itself
        self.remaining_blocks=0 # use this to count remaining blocks
        
        # Creat a row of yellow blocks
        self.yellowblocks=[]      
        for b in range(0,8):
            self.yellowblocks.append(sprite.sprite(16*b,20,16,8,sprites.yellowblock_sprite,display))
            self.remaining_blocks = self.remaining_blocks + 1
        # Create a row of red blocks
        self.redblocks=[]
        for b in range(0,8):
            self.redblocks.append(sprite.sprite(16*b,20+8,16,8,sprites.redblock_sprite,display))
            self.remaining_blocks = self.remaining_blocks + 1
        # Create a row of blue blocks
        self.blueblocks=[]
        for b in range(0,8):
            self.blueblocks.append(sprite.sprite(16*b,20+16,16,8,sprites.blueblock_sprite,display))
            self.remaining_blocks = self.remaining_blocks + 1
        # initialize the bat and ball
        self.bat=sprite.sprite(0,150,14,2,sprites.bat_sprite,display)
        self.ball=sprite.sprite(random.randrange(2,120),random.randrange(50,120),4,4,sprites.ball_sprite,display)
        self.display.clear()
        self.bonk=sound.note(500,50,0)
        self.beep=sound.note(1000,50,0)
    def play(self):
        # This is called when actual gameplay starts
        ball_x_velocity = random.choice([-1,1]) # pick a random X velocity for the ball
        ball_y_velocity = 1 # y velocity is +1 - down the screen
        # will use the ball_x and ball_y variables to manage the ball location
        ball_x = self.ball.x
        ball_y = self.ball.y
        # show the bat and the ball
        self.ball.show()
        self.bat.show()
        x=0 # this holds the x position of the bat
        moved=0 # this is used to flag movement of the bat
        start_time=time.ticks_ms() # note current time.  This is used to set the ball speed
        # show all the blocks
        for b in range(0,8):
            self.redblocks[b].show()
            self.yellowblocks[b].show()
            self.blueblocks[b].show()
        while(1):
            # This loop runs until the game ends
            if ((time.ticks_ms()-start_time) > 20): # have 20ms passed? If so then update ball position                
                start_time=time.ticks_ms() # note current time.
                ball_x = ball_x + ball_x_velocity # calculate ball's new x position
                if (ball_x > 122):	# if it at the right hand side 
                    ball_x_velocity = -1 # then make the velocity negative (heading left)
                if (ball_x < 2): # if it is at the left hand side
                    ball_x_velocity = 1 # then make the velocity positive (heading right)
                ball_y = ball_y + ball_y_velocity # calculate the ball's new y position
                if (ball_y < 2): # if it is at the top of the screen
                    ball_y_velocity = 1  # make the velocity positive (heading down)
                # check the ball's y position to see if is below the bat
                if (ball_y > self.bat.y):
                    # if it is then reset it back somewhere up the field a bit
                    self.ball.move(random.randrange(2,120),random.randrange(50,120))
                    ball_x = self.ball.x
                    ball_y = self.ball.y
                    ball_x_velocity=random.choice([-1,1])
                    self.bat.show() # re-show the bat in case it lost some pixels
                else:
                    # otherwise move the ball to it's new onscreen position
                    self.ball.move_no_erase(ball_x,ball_y)
                # did the ball hit the bat?
                if (ball_y == self.bat.y-(self.bat.height+self.ball.height-2)):
                    if ((ball_x >=self.bat.x) and (ball_x < self.bat.x+self.bat.width)):
                        # if it did then make it bounce back up the screen
                        ball_y_velocity = -1
                        self.bat.show() # re-show the bat in case it lost some pixels
                        self.snd.tune.append(self.bonk)
                # go through all of the (visible) blocks to see if they have been hit
                # by the ball.
                for b in range(0,8):
                    if (self.ball.isOverlapping(self.yellowblocks[b])==1):
                        if (self.yellowblocks[b].visible == 1):
                            # if it is hit then hide it
                            self.yellowblocks[b].hide()
                            # and decrement the remaining block counter
                            self.remaining_blocks = self.remaining_blocks - 1
                            self.snd.tune.append(self.beep)
                            ball_y_velocity = -ball_y_velocity
                    # repeat for red blocks
                    if (self.ball.isOverlapping(self.redblocks[b])==1):
                        if (self.redblocks[b].visible == 1):
                            self.redblocks[b].hide()
                            self.remaining_blocks = self.remaining_blocks - 1
                            self.snd.tune.append(self.beep)                            
                            ball_y_velocity = -ball_y_velocity
                    # repeat for blue blocks
                    if (self.ball.isOverlapping(self.blueblocks[b])==1):
                        if (self.blueblocks[b].visible == 1):
                            self.blueblocks[b].hide()
                            self.remaining_blocks = self.remaining_blocks - 1
                            self.snd.tune.append(self.beep)                           
                            ball_y_velocity = -ball_y_velocity
                # check to see if all blocks are gone
                if (self.remaining_blocks==0):
                    # if all done then display winning message
                    self.display.fillRectangle(0,0,127,159,self.display.RGBToWord(0,0,255))
                    self.display.print("You win!",0,0,self.display.RGBToWord(255,255,0),self.display.RGBToWord(0,0,255))
                    while(self.controller.aPressed()==0):
                        # Wait for user to press the A button
                        return # exit the game when they do.
            # check to see what buttons the user pressed
            if (self.controller.leftPressed()):
                if (x > 0):
                    # if left is pressed decrement x position (only if it is greater than 0)
                    x = x-1                    
                    moved = 1
            if (self.controller.rightPressed()):
                if (x < 113):
                    # if right is pressed then increment x position (only if it stays within the screen area)
                    x = x+1
                    moved = 1
            # did the bat move?
            if (moved==1):
                # if so then move it on screen
                self.bat.move_no_erase(x,self.bat.y)
                moved=0
            