#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

'''

# Import libraries -------------------------------------------------------------
import numpy as np
import random
from psychopy import data, core, event, visual
import time  # Function time-sleep()
import lines_log as log
import lines_setup as setup

# Some settings ----------------------------------------------------------------

fxc_duration = 0.5
fxc_delay = 0.05
isi = 0.5
probeDuration = 0.5
lateration = 10.0
# probedistance = 3.0
lineLength = 4.0
lineThick = 3.0

# Run setup
setup.run_setup(useGui=False)

subject_id = str(setup.participant)

# subject_id = 1
# version = 1

# Set up window
win = visual.Window(fullscr=True,
                    color='black',
                    screen=0,
                    monitor='testMonitor')


def initiate_exp():
    global instruction_objects
    global fixationCross
    global ISI
    global routineTimer
    global stimTimer
    global probeTimer
    global routine_time


    log.init(subject_id)

    # initiate instructions
    instruction_texts = setup.load_instructions()
    instruction_objects = []
    # initialize instruction slide objects:
    for i in range(len(instruction_texts)):
        instruction_text = visual.TextStim(
            win=win,
            text=instruction_texts[i],
            font='Arial',
            height=0.08,
            color='white')
        instruction_objects.append(instruction_text)


    fixationCross = visual.TextStim(win, text=u"+", height=0.08)



    ScreenHZ = win.getActualFrameRate(nIdentical=60,
                                      nMaxFrames=100,
                                      nWarmUpFrames=10,
                                      threshold=1)

    ISI = core.StaticPeriod(screenHz=ScreenHZ, win=win)
    print("Frame Rate")
    print(ScreenHZ)

    event.clearEvents(eventType='keyboard')
    win.setMouseVisible(False)

    routineTimer = core.CountdownTimer()
    stimTimer = core.CountdownTimer()
    probeTimer = core.CountdownTimer()
    routine_time = core.Clock()

def fixation_cross():

    # Routine for the fixation cross
    continueRoutine = True

    routineTimer.reset()
    routineTimer.add(fxc_duration)

    while continueRoutine:
        fixationCross.draw()
        win.flip()

        if routineTimer.getTime() < 0:
            win.flip()
            ISI.start(fxc_delay)
            ISI.complete()
            continueRoutine = False

            # check for quit (the Esc key)
        elif event.getKeys(keyList=["escape"]):
                core.quit()


def load_vertical(thisIncrement):
    global target
    global probe
    global probe2
    global lure
    global lure2
    global distance
    global direction

    direction = 'vertical'

    rand = random.randint(0, 1)

    luredistance = thisIncrement

    posTop = lineLength/2
    posBot = lineLength/-2

    if rand > 0:
        positionO = -lateration
        positionO2 = positionO-probedistance
        target = -1
        positionX = lateration
        positionX2 = positionX+luredistance

    elif rand < 1:
        positionO = lateration
        positionO2 = positionO+probedistance
        target = 1
        positionX = -lateration
        positionX2 = positionX-luredistance


    probe = visual.Line(win,
                        lineWidth=lineThick, lineColor='white',
                        start=(positionO, posTop),
                        end=(positionO, posBot),
                        ori=0,
                        units='deg')

    probe2 = visual.Line(win,
                        lineWidth=lineThick, lineColor='white',
                        start=(positionO2, posTop),
                        end=(positionO2, posBot),
                        ori=0,
                        units='deg')

    lure = visual.Line(win,
                       lineWidth=lineThick, lineColor='white',
                        start=(positionX, posTop),
                        end=(positionX, posBot),
                        ori=0,
                        units='deg')

    lure2 = visual.Line(win,
                       lineWidth=lineThick, lineColor='white',
                        start=(positionX2, lineLength/2),
                        end=(positionX2, posBot),
                        ori=0,
                        units='deg')

    distance = luredistance

def load_horizontal(thisIncrement):
    global target
    global probe
    global probe2
    global lure
    global lure2
    global distance
    global direction

    direction = 'horizontal'

    rand = random.randint(0, 1)

    luredistance = thisIncrement

    posOtop = probedistance/2
    posObot = probedistance/-2
    posXtop = luredistance/2
    posXbot = luredistance/-2


    if rand > 0:
        positionOstart = -lateration
        positionOend = -lateration-lineLength
        target = -1
        positionXstart = lateration
        positionXend = lateration+lineLength

    elif rand < 1:
        positionOstart = lateration
        positionOend = lateration + lineLength
        target = 1
        positionXstart = -lateration
        positionXend = -lateration-lineLength

    probe = visual.Line(win,
                        lineWidth=lineThick, lineColor='white',
                        start=(positionOstart, posOtop),
                        end=(positionOend, posOtop),
                        ori=0,
                        units='deg')

    probe2 = visual.Line(win,
                        lineWidth=lineThick, lineColor='white',
                        start=(positionOstart, posObot),
                        end=(positionOend, posObot),
                        ori=0,
                        units='deg')

    lure = visual.Line(win,
                       lineWidth=lineThick, lineColor='white',
                        start=(positionXstart, posXtop),
                        end=(positionXend, posXtop),
                        ori=0,
                        units='deg')

    lure2 = visual.Line(win,
                       lineWidth=lineThick, lineColor='white',
                        start=(positionXstart, posXbot),
                        end=(positionXend, posXbot),
                        ori=0,
                        units='deg')

    distance = luredistance


def instructions(instr_count):

    event.clearEvents(eventType='keyboard')
    theseKeys = []
    # win.flip()
    continueRoutine = True
    while continueRoutine == True:
        theseKeys=event.getKeys(keyList=['space', 'escape'])
        instruction_objects[instr_count].draw()
        win.flip()
        for thisKey in theseKeys:
            if thisKey == 'space':
                continueRoutine = False
                time.sleep(1)
                theseKeys = []
                win.flip()
                time.sleep(1)

            elif thisKey =='escape':
                core.quit()


def run_trials(in_block):
    trial = 0
    block = in_block

    fixationCross.setAutoDraw(True)
    staircase = data.StairHandler(startVal = probedistance*2,
                            nReversals=7,
                            stepType = 'lin',
                            stepSizes=[probedistance*0.4,
                                       probedistance*0.2,
                                       probedistance*0.1,
                                       probedistance*0.1,
                                       probedistance*0.05,
                                       probedistance*0.05,
                                       probedistance*0.02],
                            nUp=1, nDown=3,  # will home in on the 80% threshold
                            nTrials=1,
                            maxVal=probedistance*2, minVal=probedistance+0.01)

    for thisIncrement in staircase:

        win.flip()

        theseKeys = []
        event.clearEvents(eventType='keyboard')
        ISI.start(isi)

        trial = trial + 1
        startProbe = True
        startResponse = False
        thisResp = '.'
        rt = '.'

        if vertical == True:
            load_vertical(thisIncrement)
        elif vertical == False:
            load_horizontal(thisIncrement)


        ISI.complete()

        routineTimer.reset()
        routineTimer.add(probeDuration)

        while routineTimer.getTime() > 0:
            probe.draw()
            probe2.draw()
            lure.draw()
            lure2.draw()
            win.flip()

            if routineTimer.getTime() < 0:
                startProbe = False
                startResponse = True
                routine_time.reset()
                win.flip()

                while startResponse == True:
                    t = routine_time.getTime()
                    theseKeys = event.waitKeys(keyList=['a', 'l', 'escape'])

                    for thisKey in theseKeys:
                        if thisKey == 'a':
                            if target == -1: thisResp = 1
                            else: thisResp = 0

                        if thisKey == 'l':
                            if target == 1: thisResp = 1
                            else: thisResp = 0

                        elif thisKey == 'escape':
                                core.quit()

                    staircase.addResponse(thisResp)
                    # print(dir(staircase))
                    startResponse = False
                    rt = t

        ISI.start(isi)

        revInt = staircase.reversalIntensities
        revPoint = staircase.reversalPoints

        reversal = len(revPoint)

        rev = 0
        if len(revPoint) > 0:
            if revPoint[-1] == trial - 1:
                rev = 1

            else: rev = 0

        log.log(block,
                direction,
                probedistance,
                trial,
                target,
                rev,
                distance,
                thisResp,
                rt)
        ISI.complete()

    fixationCross.setAutoDraw(False)

def run_exp():
    global vertical
    global probedistance

    initiate_exp()
    instructions(0)

    probedistance = 3.0 # needs to be numeric
    vertical = True # vertical
    run_trials(1)
    instructions(1)

    vertical = False # horizontal
    run_trials(2)
    instructions(1)


    probedistance = 1.5 # needs to be numeric
    vertical = True
    run_trials(3)
    instructions(1)

    vertical = False
    run_trials(4)
    instructions(2)

run_exp()
