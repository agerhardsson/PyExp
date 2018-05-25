#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from psychopy import visual, core, event
from CustomMouse import CustomMouse
import numpy

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


# Set axis labels
# Arousal
high = 'Stark'
low = 'Svag'

# valenceX
right = 'Positive'
left = 'Negative'


# ------------------Routine definitions--------------------------------------
def initialize_components():
    global routineTimer
    global routine_time
    global routine_time2
    global fixSpot
    global markerSpot
    global axis
    global mouse
    global Mymouse
    global leftLim
    global rightLim
    global topLim
    global bottomLim

    routineTimer = core.CountdownTimer()  # track time left of each routine
    routine_time = core.Clock()  # local routine time


    fixSpot = visual.TextStim(win=win,
                              ori=0,
                              name='fxc',
                              text='+',
                              font='Arial',
                              alignHoriz='center',
                              pos=[0, 0],
                              height=0.10,
                              wrapWidth=1,
                              color='black',
                              colorSpace='rgb',
                              opacity=1)

    markerSpot = visual.TextStim(win=win,
                                 ori=0,
                                 name='fxc',
                                 text='+',
                                 font='Arial',
                                 alignHoriz='center',
                                 pos=[0, 0],
                                 height=0.10,
                                 wrapWidth=1,
                                 color='black',
                                 colorSpace='rgb',
                                 opacity=1)

    axis = []

    arousalY = visual.Line(win,
                           start=(-0.5, 0),
                           end=(0.5, 0),
                           lineColor='black',
                           size=1,
                           lineWidth=1)
    axis.append(arousalY)

    arousal_high = visual.TextStim(win=win,
                                   ori=0,
                                   name='fxc',
                                   text=high,
                                   font='Arial',
                                   alignHoriz='center',
                                   pos=[0, 0.6],
                                   height=0.10,
                                   wrapWidth=1,
                                   color='black',
                                   colorSpace='rgb',
                                   opacity=1)
    axis.append(arousal_high)

    arousal_low = visual.TextStim(win=win,
                                  ori=0,
                                  name='fxc',
                                  text=low,
                                  font='Arial',
                                  alignHoriz='center',
                                  pos=[0, -0.6],
                                  height=0.10,
                                  wrapWidth=1,
                                  color='black',
                                  colorSpace='rgb',
                                  opacity=1)
    axis.append(arousal_low)

    valenceX = visual.Line(win,
                           start=(0, -0.5),
                           end=(0, 0.5),
                           lineColor='black',
                           size=1,
                           lineWidth=1)
    axis.append(valenceX)

    valence_right = visual.TextStim(win=win,
                                    ori=0,
                                    name='fxc',
                                    text=right,
                                    font='Arial',
                                    alignHoriz='left',
                                    pos=[0.51, 0],
                                    height=0.10,
                                    wrapWidth=1,
                                    color='black',
                                    colorSpace='rgb',
                                    opacity=1)

    axis.append(valence_right)

    valence_left = visual.TextStim(win=win,
                                   ori=0,
                                   name='fxc',
                                   text=left,
                                   font='Arial',
                                   alignHoriz='right',
                                   pos=[-0.51, 0],
                                   height=0.10,
                                   wrapWidth=1,
                                   color='black',
                                   colorSpace='rgb',
                                   opacity=1)

    frame = visual.Rect(win,
                        width=1,
                        height=1,
                        lineColor='black')
    axis.append(frame)

    axis.append(valence_left)

    mouse = visual.CustomMouse(win,
                               leftLimit=-0.5,
                               topLimit=0.5,
                               rightLimit=0.5,
                               bottomLimit=-0.5,
                               pointer=None,
                               visible=True)

    leftLim = -0.5
    topLim = 0.5
    rightLim = 0.5
    bottomLim = -0.5


def Response_axis():

    event.clearEvents(eventType='keyboard')

    for a in range(0, len(axis)):
        axis[a].setAutoDraw(True)

    continueRoutine = True
    press = False
    responseY = '.'
    responseX = '.'
    rt = 0
    mouse.clickReset()
    markerSpot.setPos(mouse.getPos())
    markerSpot.setAutoDraw(True)
    routine_time.reset()

    while continueRoutine is True:
        mouse1, mouse2, mouse3 = mouse.getPressed()

        dx, dy = mouse.getPos()
        x = min(max(dx, leftLim), rightLim)
        y = min(max(dy, bottomLim), topLim)
        lastPos = numpy.array([x, y])

        rt = routine_time.getTime()

        win.flip()
        if (dx > rightLim or dx < leftLim or
           dy > topLim or dy < bottomLim):
            mouse.setPos(lastPos)
            within = False
        else:
            markerSpot.setPos(mouse.getPos())
            within = True

        if mouse1 and press is False and within is True:
            fixSpot.setAutoDraw(True)
            fixSpot.setPos(mouse.getPos())
            responseY = str(mouse.getPos()[0]*2*10)
            responseX = str(mouse.getPos()[1]*2*10)
            reaction_time = str(rt)
            markerSpot.setAutoDraw(False)

            press = True

            routineTimer.reset()
            routineTimer.add(1.5)  # time to wait after press

        # Wait for press and delay then quit
        if press is True and routineTimer.getTime() < 0:
            continueRoutine = False

        if event.getKeys(keyList=["escape"]):
            core.quit()
    print(responseX)
    print(responseY)
    print(reaction_time)


initialize_components()
Response_axis()
