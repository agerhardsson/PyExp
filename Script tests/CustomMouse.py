#!/usr/bin/env python

# demo of CustomMouse()
# author Jeremy Gray

from psychopy import visual, event
import numpy

class CustomMouse():
    """Class for more control over the mouse, including the pointer graphic and a bounding box.

    Not well tested. Known limitations / bugs:
    - getRel() always returns [0,0], maybe that's ok
    - mouseMoved is always False, no idea why, seems bad
    - unsure if clickReset() does anything
    - resetting the limits does not always take effect fully
    """
    def __init__(self, win, newPos=None, visible=True,
                 leftLimit=None, topLimit=None, rightLimit=None, bottomLimit=None,
                 pointer=None):
        self.win = win
        self.mouse = event.Mouse(win=self.win)
        # partial Mouse.__init__
        self.lastPos = None
        self.prevPos = None
        self.getRel = self.mouse.getRel
        self.getWheelRel = self.mouse.getWheelRel
        self.mouseMoved = self.mouse.mouseMoved  # FAILS
        self.mouseMoveTime = self.mouse.mouseMoveTime
        self.getPressed = self.mouse.getPressed
        self.clickReset = self.mouse.clickReset  # ???
        self._pix2windowUnits = self.mouse._pix2windowUnits # ???
        self._windowUnits2pix = self.mouse._windowUnits2pix # ???

        # the graphic to use as the 'mouse' icon (pointer)
        if pointer:
            self.setPointer(pointer)
        else:
            self.pointer = visual.TextStim(win, text='+', height=.08)
        self.mouse.setVisible(False) # hide the system mouse
        self.visible = visible # the custom mouse

        if type(leftLimit) in [int,float]: self.leftLimit = leftLimit
        else: self.leftLimit = -1
        if type(rightLimit) in [int,float]: self.rightLimit = rightLimit
        else: self.rightLimit = 1
        if type(topLimit) in [int,float]: self.topLimit = topLimit
        else: self.topLimit = 1
        if type(bottomLimit) in [int,float]: self.bottomLimit = bottomLimit
        else: self.bottomLimit = -1
        if newPos is not None:
            self.x, self.y = newPos
        else:
            self.x = self.y = 0
    def setPos(self):
        self.pointer.setPos(self.getPos())
    def getPos(self):
        dx, dy = self.getRel()
        self.x = min(max(self.x+dx, self.leftLimit), self.rightLimit)
        self.y = min(max(self.y+dy, self.bottomLimit), self.topLimit)
        self.lastPos = numpy.array([self.x, self.y])
        return self.lastPos
    def draw(self):
        self.setPos()
        if self.visible:
            self.pointer.draw()
    def getVisible(self):
        return self.visible
    def setVisible(self, visible):
        self.visible = visible
    def setPointer(self, pointer):
        if 'draw' in dir(pointer) and 'setPos' in dir(pointer):
            self.pointer = pointer
        else:
            raise AttributeError, "need .draw() and setPos() methods in pointer for CustomMouse"

#
#    end of the class, start of the demo:


myWin = visual.Window()
vm = CustomMouse(myWin, leftLimit=0, topLimit=0, rightLimit=0.3, bottomLimit=-0.3)
instr = visual.TextStim(myWin,text="move the mouse around\nclick to release the mouse bound")
new_pointer = visual.TextStim(myWin,text='o') # anything with .draw() and .setPos(), like PatchStim()

while not 'escape' in event.getKeys():
    instr.draw()
    vm.draw()
    myWin.flip()
    if vm.getPressed()[0]:
        #vm.setVisible(not vm.getVisible()) # click toggles mouse visibility via get/set
        print "[%.2f, %.2f]" % (vm.getPos()[0],vm.getPos()[1]),
        print vm.getRel(), vm.getWheelRel(), "%.3f"%vm.mouseMoveTime()
        vm.leftLimit = vm.bottomLimit = -1
        vm.rightLimit = vm.topLimit = 1
        instr.setText("press 'escape' to quit")
        vm.pointer = new_pointer
