class sprite:
    def __init__(self,x,y,w,h,image,display):
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.image=image
        self.visible=0
        self.display=display
        self.horiz=1 # default orientation left to right
        self.vert=1  # default orientation top to bottom
    def show(self):
        self.display.putImage(self.x,self.y,self.width,self.height,self.image,self.horiz,self.vert)
        self.visible=1
    def hide(self):
        self.display.fillRectangle(self.x,self.y,self.width,self.height,0)
        self.visible=0
    def move(self,newx, newy):
        if (self.visible==1):
            self.hide()
        self.x = newx
        self.y = newy
        self.show()
    def move_no_erase(self,newx, newy):
        self.x = newx
        self.y = newy
        self.show()
    def setOrientation(self, horiz, vert):
        self.horiz = horiz
        self.vert = vert
    def isOverlapping(self,sprite2):
        # Check to see if sprite2 overlaps this sprite in any way.
        # The approach here is to see if any of the corners of this are inside
        # the bounding rectangle of sprite2.
        isWithin=0
        xt=self.x
        yt=self.y        
        if ( (xt >= sprite2.x) and (xt <= sprite2.x+sprite2.width)):
            if ( (yt >= sprite2.y) and (yt <= sprite2.y+sprite2.height)):
                isWithin=1
        xt=self.x+self.width
        yt=self.y        
        if ( (xt >= sprite2.x) and (xt <= sprite2.x+sprite2.width)):
            if ( (yt >= sprite2.y) and (yt <= sprite2.y+sprite2.height)):
                isWithin=1
        xt=self.x
        yt=self.y+self.height        
        if ( (xt >= sprite2.x) and (xt <= sprite2.x+sprite2.width)):
            if ( (yt >= sprite2.y) and (yt <= sprite2.y+sprite2.height)):
                isWithin=1        

        xt=self.x+self.width
        yt=self.y+self.height        
        if ( (xt >= sprite2.x) and (xt <= sprite2.x+sprite2.width)):
            if ( (yt >= sprite2.y) and (yt <= sprite2.y+sprite2.height)):
                isWithin=1        
        return isWithin        