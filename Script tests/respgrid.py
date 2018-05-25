#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from psychopy import visual, core, event


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


# ------------------Routine definitions--------------------------------------
def initialize_components():
    global routineTimer
    global routine_time
    global fixSpot
    global markerSpot

    routineTimer = core.CountdownTimer()  # track time left of each routine
    routine_time = core.Clock()  # local routine time

    fixSpot = visual.GratingStim(win,
                                 tex="none",
                                 mask="gauss",
                                 pos=(0, 0),
                                 size=(0.05, 0.05),
                                 color='black',
                                 autoLog=False)


    markerSpot = visual.GratingStim(win,
                                 tex="none",
                                 mask="gauss",
                                 pos=(0, 0),
                                 size=(0.05, 0.05),
                                 color='black',
                                 autoLog=False)
def Response_grid():
    mouse = event.Mouse(visible=False)

    event.clearEvents(eventType='keyboard')

    t = 0
    routine_time.reset()
    routineTimer.reset()
    routineTimer.add(10)
    win.flip()
    mouse.clickReset()
    mouse.setPos()
    continueRoutine = True
    press = False
    response = []


    while continueRoutine is True and t < 10:
        mouse_dX, mouse_dY = mouse.getRel()
        mouse1, mouse2, mouse3 = mouse.getPressed()

        # get current time
        t = routine_time.getTime()
        markerSpot.draw()

        markerSpot.setPos(mouse.getPos())

        if mouse1 and press is False:
            fixSpot.setPos(mouse.getPos())
            response = mouse.getPos()
            press = True

        # *matrix1_WM6_training* updates
        if t >= 10:
            continueRoutine = False

        if event.getKeys(keyList=["escape"]):
            core.quit()

        fixSpot.draw()
        win.flip()

    print(mouse3)
    print(response)
initialize_components()
Response_grid()
