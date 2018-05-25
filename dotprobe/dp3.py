#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

'''



# Import libraries -------------------------------------------------------------
import numpy as np
import random
from psychopy import data, core, event, visual
import time  # Function time-sleep()
import dp_log as log
import dp_setup as setup

# ------------------------------------------------------------------------------
fxc_duration = 0.5
fxc_delay = 0.05
isi = 0.5
probeDuration = 0.5
# Run setup

# setup.run_setup(useGui=False)
#
# subject_id = str(setup.participant)
# version = str(setup.version)

subject_id = 1
version = 1

lateration = 0.4

# Probability of target

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


    log.init(subject_id, version)

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


def load_grating():
    global target
    global probe
    global lure
    # global lure_ori

    rand = random.randint(0, 1)

    if rand > 0:
        positionO = -lateration
        target = -1
        positionX = lateration
    elif rand < 1:
        positionO = lateration
        target = 1
        positionX = -lateration

    probe = visual.Line(win,
                        lineWidth=1.5, lineColor='white',
                        start=(positionO, -0.1),
                        end=(positionO, 0.1),
                        ori=0)

    lure_ori = random.random()/100

    lure = visual.Line(win,
                       lineWidth=1.5, lineColor='white',
                        start=(positionX-lure_ori, -0.1),
                        end=(positionX+lure_ori, 0.1),
                        ori=0)

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


def run_trials(n_trials):
    trial = 0
    continueRoutine = True
    event.clearEvents(eventType='keyboard')
    theseKeys = []
    while continueRoutine:
        for trial in range(n_trials + 1):
            if trial == n_trials:
                    continueRoutine = False
                    break

            win.flip()

            ISI.start(isi)

            trial = trial + 1
            startProbe = True
            startResponse = False
            thisResp = '.'
            rt = '.'

            # load_dot()
            load_grating()

            ISI.complete()

            fixation_cross()
            routineTimer.reset()
            routineTimer.add(probeDuration)

            while routineTimer.getTime() > 0:
                probe.draw()
                lure.draw()
                win.flip()

                if routineTimer.getTime() < 0:
                    startProbe = False
                    startResponse = True
                    routine_time.reset()
                    win.flip()

                    while startResponse == True:
                        t = routine_time.getTime()
                        theseKeys = event.waitKeys(keyList=['a', 'l'])

                        for thisKey in theseKeys:
                            if thisKey == 'a':
                                thisResp = -1
                            elif thisKey == 'l':
                                thisResp = 1
                                
                        startResponse = False
                        ISI.start(0.1)
                        theseKeys = []
                        event.clearEvents(eventType='keyboard')
                        rt = t
                        ISI.complete()

                if event.getKeys(keyList=["escape"]):
                    core.quit()

            # log.log(trial, target, haspos, saspos, thisResp, rt)

def run_exp():
    initiate_exp()
    log.set_start_version(str(version))
    instructions(0)

    run_trials(30)
    instructions(1)

    log.next_block()
    run_trials(30)
    instructions(1)

    log.next_block()
    run_trials(30)
    instructions(1)

    log.next_block()
    run_trials(30)
    instructions(2)

run_exp()
