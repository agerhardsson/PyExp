#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules --------------------------------------------------------------
from __future__ import division  # handy tool for division

import time, os

from psychopy import visual, core, event

from joso_setup import *

from joy_sorrow_log import *

import scales

# Settings --------------------------------------------------------------------

WinWidth = 800
WinHeigth = 600
FullScreen = True
text_size = 0.07
BGcol = 'black'

# Max experiment time
max_time = 30 # in minutes

# Inter stimuli interval
isi = 0.500
# Fixation cross duration:
fxc_duration = 2.400

# Fixation cross delay (after fxc):
fxc_delay = 0.100

# Scale delay
scale_delay = 2.00

# Number of trials
n_trials = 5

pic_size = [1.2, 1.3]
# Load log --------------------------------------------------------------------
subject_id, version, load_set, run_training = run_setup(useGui=False)

# Set up window ---------------------------------------------------------------
win = visual.Window(
    size=(WinWidth, WinHeigth),
    fullscr=FullScreen,
    monitor='testMonitor',
    allowGUI=True,
    checkTiming=True,
    color=BGcol
)

# initialize components --------------------------------------------------------

instruction_texts = instructions()

# add additional instructions to dictionary
instruction_texts['training_start'] = u'Först en träningsomgång!'
instruction_texts['training_end'] =  u'Slut på träning'

# scales -----------------------------------------------------------------
kss = scales.kss(win, subject_id=subject_id, use_mouse=False)
panas = scales.panas(win, subject_id=subject_id, textheight=0.05)

# Create Stim objects ----------------------------------------------------------
instruction_object = visual.TextStim(
    win=win,
    text='',
    font='Arial',
    height=text_size,
    wrapWidth=1.8,
    color='white')

fixationCross = visual.TextStim(
    win=win,
    text='+',
    font='Arial',
    pos=[0, 0.2],
    height=0.18,
    wrapWidth=1.8,
    color='white')

arrow = visual.ImageStim(
    win=win,
    name='stimuli',
    image='images/arrows.png',
    mask=None,
    pos=[0.5, -0.5])


# Initialize scales -----------------------------------------------------------
sorrow_joy = visual.TextStim(
    win=win,
    text=u'Upplever du en känsla av...?',
    font='Arial',
    pos=[0, -0.6],
    height=text_size,
    wrapWidth=1.8,
    color='white')

marker = visual.TextStim(
    win=win,
    text='',
    units="norm",
    bold=True,
    color="white")

rs = visual.RatingScale(
    win=win,
    low=1,
    high=9,
    labels=[u'Sorg', u'Neutral', u'Glädje'],
    marker='triangle',
    scale=None,
    markerColor='white',
    size=0.8,
    markerStart=5,
    lineColor='white',
    leftKeys='left',
    rightKeys = 'right',
    acceptKeys='down',
    pos=[0.0, -0.7],
    showAccept=False
    )

# Frame rate  for ISI ----------------------------------------------------------
ScreenHZ = win.getActualFrameRate(nIdentical=60,
                                  nMaxFrames=100,
                                  nWarmUpFrames=10,
                                  threshold=1)

ISI = core.StaticPeriod(screenHz=ScreenHZ, win=win)
print "Frame Rate: " + str(ScreenHZ)

# Create timers ----------------------------------------------------------------
routineTimer = core.CountdownTimer()
expTimer = core.CountdownTimer()
routine_time = core.Clock()

# Define instructions function -------------------------------------------------
def instructions(instr, time=60):
    win.setMouseVisible(False)
    event.clearEvents(eventType='keyboard')

    instruction_object.setText(instruction_texts[instr])

    routineTimer.reset()
    routineTimer.add(time)

    while not event.getKeys(keyList=['space']):
        instruction_object.draw()
        win.flip()
        if routineTimer.getTime() < 0:
            break
        if event.getKeys(keyList=['escape']):
            core.quit()

    core.wait(0.5)

# Fixation cross --------------------------------------------------------------
def fixation_cross():
    win.setMouseVisible(False)

    routineTimer.reset()
    routineTimer.add(fxc_duration)

    while routineTimer.getTime() > 0:
        fixationCross.draw()
        win.flip()
        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()
    core.wait(fxc_delay)


def main_block(n_trials):

    time_stamp = 0
    trial = 0

    for trial in range(n_trials + 1):
        if trial == n_trials:
            break
        elif expTimer.getTime() < 0:
            continueRoutine = False
            break
        ISI.start(isi)
        trial = trial + 1
        image_path = return_next_picture()
        # initialize current stimuli:
        stimuli = visual.ImageStim(
            win=win,
            name='stimuli',
            image=image_path,
            pos=[0, 0.2],
            size=pic_size,
            interpolate=True)
        t = 0
        rs.reset()
        ISI.complete()
        win.flip()
        fixation_cross()
        routine_time.reset()  # clock

        while rs.noResponse:
            t = routine_time.getTime()
            stimuli.draw()
            win.flip()

            if t > scale_delay:
                sorrow_joy.draw()
                rs.draw()
            ISI.start(1.5)

            # check for quit (the Esc key)
            if event.getKeys(keyList=["escape"]):
                core.quit()

        answer = str(rs.getRating())
        rt = str(rs.getRT())
        time_stamp = str(expTimer.getTime())

        log_event(answer, rt, time_stamp, trial)
        ISI.complete()

# Run experiment --------------------------------------------------------------

def run_main_exp():
    log_init(version, load_set, subject_id, run_training)
    panas.draw()
    kss.draw()
    instructions('intro1')
    expTimer.reset()
    expTimer.add(max_time*60)

    # Training block
    if run_training == True:
        instructions('intro2')
        instructions('training_start', 3)
        main_block(5)
        instructions('training_end', 3)
    # Block 1
    next_block()
    instructions('intro2')          # Instruction
    main_block(n_trials)            # Experiment block 1

    # Block 2
    instructions('intermed')        # Instruction
    kss.draw()                      # kss rating scale
    next_block()                    # next block
    main_block(n_trials)            # Experiment block 2

    # Block 3
    instructions('intermed')        # Instruction
    kss.draw()                      # kss rating scale
    next_block()                    # next block
    main_block(n_trials)            # Experiment block 3
    panas.draw()
    panas.logFile()
    kss.logFile()
    instructions('end')             # Instruction

run_main_exp()

win.close()
