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
fxc_duration = 5.0
fxc_delay = 0.1
isi = 2.5
stimuliDuration = 1.0
probeDuration = 2.0
# Run setup
# setup.run_setup(useGui=False)

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


def load_image():
    global sas_stim
    global has_stim
    global haspos
    global saspos

    log.next_row()

    img_path = "pics/" + log.next_sad()
    sas_stim = visual.ImageStim(
        win=win,
        name='stimuli',
        image=img_path,
        mask='gauss',
        maskParams=None,
        pos=[0, 0],
        interpolate=True)

    img_path = "pics/" + log.next_happy()
    has_stim = visual.ImageStim(
        win=win,
        name='stimuli',
        image=img_path,
        mask='gauss',
        maskParams=None,
        pos=[0, 0],
        interpolate=True)

    rand = random.randint(0, 1)

    if rand > 0:
        positionH = -lateration
        haspos = -1
        positionS = lateration
        saspos = 1
    elif rand < 1:
        positionH = lateration
        haspos = 1
        positionS = -lateration
        saspos = -1

    has_stim.setPos(newPos=[positionH, 0.0])
    sas_stim.setPos(newPos=[positionS, 0.0])

def load_dot():
    global target
    global odot
    global xdot

    rand = random.randint(0, 1)

    if rand > 0:
        positionO = -lateration
        target = -1
        positionX = lateration
    elif rand < 1:
        positionO = lateration
        target = 1
        positionX = -lateration

    odot = visual.TextStim(win, text=u"O", height=0.08, pos=[positionO, 0.0])
    xdot = visual.TextStim(win, text=u"X", height=0.08, pos=[positionX, 0.0])

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
    while continueRoutine:
        for trial in range(n_trials + 1):
            if trial == n_trials:
                    continueRoutine = False
                    break

            win.flip()

            ISI.start(isi)

            event.clearEvents(eventType='keyboard')
            theseKeys = []
            trial = trial + 1
            probeStart = False
            thisResp = '.'
            rt = '.'

            load_dot()
            load_image()

            ISI.complete()

            fixation_cross()

            routineTimer.reset()
            routineTimer.add(stimuliDuration + probeDuration)

            while routineTimer.getTime() > 0:
                if routineTimer.getTime() > probeDuration:
                    stimStart = True
                    has_stim.draw()
                    sas_stim.draw()
                    win.flip()

                elif routineTimer.getTime() < probeDuration:
                    routine_time.reset()
                    startProbe = True
                    win.flip()

                    while routineTimer.getTime() > 0 and startProbe== True:
                        t = routine_time.getTime()
                        theseKeys = event.getKeys(keyList=['a', 'l', 'escape'])
                        odot.draw()
                        xdot.draw()
                        win.flip()

                        for thisKey in theseKeys:
                            if thisKey == 'a':
                                thisResp = -1
                            elif thisKey == 'l':
                                thisResp = 1

                            rt = t

                if event.getKeys(keyList=["escape"]):
                    core.quit()

            log.log(trial, target, haspos, saspos, thisResp, rt)
            if continueRoutine:
                event.clearEvents(eventType='keyboard')
                # win.flip()
initiate_exp()
log.set_start_version(str(version))
run_trials(10)
# instructions(2)
# fixation_cross()
