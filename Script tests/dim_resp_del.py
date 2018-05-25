#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from psychopy import visual, core, event
import numpy


class dimscale():
    # ------------------Routine definitions--------------------------------------
    def __init__(self,
                 window,
                 size=0.5,
                 left=-0.5,
                 top=0.5,
                 right=0.5,
                 bottom=-0.5,
                 high='Stark',
                 low='Svag',
                 pos='Positiv',
                 neg='Negativ',
                 txsize=0.10):
        self.win=window
        self.left=left
        self.top=top
        self.right=right
        self.bottom=bottom
        self.txsize=0.10
        # Arousal
        self.high = 'Stark'
        self.low = 'Svag'

        # Valence
        self.pos = 'Positiv'
        self.neg = 'Negativ'

        self.axis = []
        self.arousalY = visual.Line(win=self.win,
                                    start=(self.bottom, 0),
                                    end=(self.top, 0),
                                    lineColor='black',
                                    size=1,
                                    lineWidth=1)
        self.axis.append(self.arousalY)
        self.arousal_high = visual.TextStim(win=self.win,
                                            ori=0,
                                            name='txt',
                                            text=self.high,
                                            font='Arial',
                                            alignHoriz='center',
                                            pos=[0, self.top + 0.1],
                                            height=txsize,
                                            wrapWidth=1,
                                            color='black',
                                            colorSpace='rgb',
                                            opacity=1)
        self.axis.append(self.arousal_high)
        self.arousal_low = visual.TextStim(win=self.win,
                                      ori=0,
                                      name='txt',
                                      text=self.low,
                                      font='Arial',
                                      alignHoriz='center',
                                      pos=[0, self.bottom - 0.1],
                                      height=txsize,
                                      wrapWidth=1,
                                      color='black',
                                      colorSpace='rgb',
                                      opacity=1)
        self.axis.append(self.arousal_low)
        self.valenceX = visual.Line(win=self.win,
                               start=(0, self.left),
                               end=(0, self.right),
                               lineColor='black',
                               size=1,
                               lineWidth=1)
        self.axis.append(self.valenceX)
        self.valence_right = visual.TextStim(win=self.win,
                                        ori=0,
                                        name='txt',
                                        text=self.pos,
                                        font='Arial',
                                        alignHoriz='left',
                                        pos=[self.right + 0.01, 0],
                                        height=txsize,
                                        wrapWidth=1,
                                        color='black',
                                        colorSpace='rgb',
                                        opacity=1)

        self.axis.append(self.valence_right)
        self.valence_left = visual.TextStim(win=self.win,
                                       ori=0,
                                       name='txt',
                                       text=self.neg,
                                       font='Arial',
                                       alignHoriz='right',
                                       pos=[self.left - 0.01, 0],
                                       height=txsize,
                                       wrapWidth=1,
                                       color='black',
                                       colorSpace='rgb',
                                       opacity=1)
        self.axis.append(self.valence_left)
        self.frame = visual.Rect(win=self.win,
                            width=self.right*2,
                            height=self.top*2,
                            lineColor='black')
        self.axis.append(self.frame)
        self.mouse = visual.CustomMouse(win=self.win,
                                   leftLimit=self.left,
                                   topLimit=self.top,
                                   rightLimit=self.right,
                                   bottomLimit=self.bottom,
                                   pointer=None,
                                   visible=True)
        self.mouse.pointer = visual.TextStim(win=self.win,
                                        text='+',
                                        color='black',
                                        height=txsize,)


    def paint_dim(self):
        for a in range(0, len(self.axis)):
            self.axis[a].setAutoDraw(True)

    def init_response(self):
        self.mouse.clickReset()
        self.press = False
        self.x = '.'
        self.y = '.'
        self.routine_time = core.Clock()

    def return_response(self):
        return [self.x, self.y, self.rt]

    def run_scale(self):
        self.paint_dim()
        self.init_response()
        self.continueRoutine = True
        self.press = False

        while self.continueRoutine is True and self.press is False:
            self.t = self.routine_time.getTime()
            self.mouse1, self.mouse2, self.mouse3 = self.mouse.getPressed()
            if not self.mouse1 and self.press is False:
                self.mouse.draw()
                self.win.flip()

            if self.mouse1 and self.press is False:
                self.x = str(self.mouse.getPos()[0]*10/self.right)
                self.y = str(self.mouse.getPos()[1]*10/self.top)
                self.rt = self.t
                self.press = True
                core.wait(1.5)

            # Wait for press and delay then quit
            if self.press is True:
                self.continueRoutine = False

            if event.getKeys(keyList=["escape"]):
                core.quit()
        self.return_response()


# Setup the Window
win = visual.Window(fullscr=True,
                    screen=0,
                    allowGUI=False,
                    allowStencil=False,
                    monitor='testMonitor',
                    color='grey',
                    colorSpace='rgb',
                    blendMode='avg',
                    useFBO=True)

scale = dimscale(win,
                 left=-0.5,
                 top=0.5,
                 right=0.5,
                 bottom=-0.5,
                 txsize=0.05)

scale.run_scale()
valence = scale.return_response()[0]
arousal = scale.return_response()[1]
reaction_time = scale.return_response()[2]

print valence
print arousal
print reaction_time
