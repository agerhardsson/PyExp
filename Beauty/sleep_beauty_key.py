#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules --------------------------------------------------------------
from __future__ import division  # handy tool for division

import time

from psychopy import visual, core, event

import beauty_setup as setup

from sleep_beauty_log import *

from kss_query import kss_class

from survey_art import *

# Settings --------------------------------------------------------------------

WinWidth = 1280
WinHeigth = 800
FullScreen = True
text_size = 0.07
BGcol = 'black'

# Fixation cross duration:
fxc_duration = 1.250000

# Fixation cross delay (after fxc):
fxc_delay = 0.250000

# Stimuli duration time
stim_duration = 1.000000

# Inter stimuli interval
isi = 1.000000

# Number of trials
n_trials = 2

pic_size = [1.1, 1.1]
# Run art survey
run_survey = False

# Load setup --------------------------------------------------------------------
setup.run_setup(useGui=False)
# log -------------------------------------------------------------------------
subject_id = str(setup.participant)
version = str(setup.version)
load_set = str(setup.load_set)
run_version = setup.run_version
run_training = setup.run_training

# Save info about subject_id and version to the logging script: ---------------
set_subject_id(subject_id)
set_version(version)
set_load_set(load_set)

# Set up window ---------------------------------------------------------------
win = visual.Window(
    size=(WinWidth, WinHeigth),
    fullscr=FullScreen,
    monitor='testMonitor',
    allowGUI=True,
    checkTiming=True,
    color=BGcol
)

# Initialize scales -----------------------------------------------------------
kss = kss_class(win=win, subject_id=subject_id,
                textcol='white', use_mouse=False)

survey = suvery(win=win, subject_id=subject_id,
                text_size=text_size)


def initialize_components():
    global instruction_objects
    global fixationCross
    global routineTimer
    global routine_time
    global ISI
    global key_response
    global buttons
    global valence
    global beauty_question
    global training_text1
    global training_text2
    global yes_response
    global no_response
    global rs
    global sorrow_joy
    global marker
    global arrow

    # load instruction slide texts to a list:
    instruction_texts = setup.load_instructions()

    instruction_objects = []
    # initialize instruction slide objects:
    for i in range(len(instruction_texts)):
        instruction_text = visual.TextStim(
            win=win,
            ori=0,
            name='instruction',
            text=instruction_texts[i],
            font='Arial',
            alignHoriz='center',
            pos=[0, 0],
            height=text_size,
            wrapWidth=1.8,
            color='white',
            colorSpace='rgb',
            opacity=1)
        instruction_objects.append(instruction_text)

    arrow = visual.ImageStim(
        win=win,
        name='stimuli',
        image='images/arrows.png',
        mask=None,
        ori=0,
        pos=[0.3, 0.45])

    training_text1 = visual.TextStim(
        win=win,
        ori=0,
        name='beauty_question',
        text=u'Först en träningsomgång',
        font='Arial',
        alignHoriz='center',
        pos=[0.0, 0.0],
        height=0.08,
        wrapWidth=1.8,
        color='white',
        colorSpace='rgb',
        opacity=1)
    training_text2 = visual.TextStim(
        win=win,
        ori=0,
        name='beauty_question',
        text=u'Slut på träning',
        font='Arial',
        alignHoriz='center',
        pos=[0.0, 0.0],
        height=0.08,
        wrapWidth=1.8,
        color='white',
        colorSpace='rgb',
        opacity=1)

    # initialize fixationCross:
    fixationCross = visual.TextStim(
        win=win,
        ori=0,
        name='fxc',
        text='+',
        font='Arial',
        alignHoriz='center',
        pos=[0, 0.2],
        height=0.20,
        wrapWidth=1.8,
        color='white',
        colorSpace='rgb',
        opacity=1)

    beauty_question = visual.TextStim(
        win=win,
        ori=0,
        name='beauty_question',
        text=u'Upplever du en känsla av skönhet?',
        font='Arial',
        alignHoriz='center',
        pos=[0, -0.6],
        height=0.07,
        wrapWidth=1.8,
        color='white',
        colorSpace='rgb',
        opacity=1)

    sorrow_joy = visual.TextStim(
        win=win,
        ori=0,
        name='beauty_question',
        text=u'Fick du en känsla av...?',
        font='Arial',
        alignHoriz='center',
        pos=[0, -0.6],
        height=0.07,
        wrapWidth=1.8,
        color='white',
        colorSpace='rgb',
        opacity=1)

    yes_response = visual.TextStim(
        win=win,
        name='yes_response',
        text=u'Ja',
        pos=[-0.1, -0.76],
        height=0.06,
        color='white',
        colorSpace='rgb')
    no_response = visual.TextStim(
        win=win,
        name='no_response',
        text=u'Nej',
        pos=[0.1, -0.76],
        height=0.06,
        color='white',
        colorSpace='rgb')
    marker = visual.TextStim(
        win=win,
        text='*',
        units="norm"
    )

    rs = visual.RatingScale(
        win=win,
        low=1,
        high=7,
        labels=[u'Glädje', u'Neutral', u'Sorg'],
        marker=marker,
        scale=None,
        markerColor='white',
        size=0.8,
        markerStart=4,
        lineColor='white',
        leftKeys='left',
        rightKeys='right',
        acceptKeys='',
        pos=[0.0, -0.7],
        showAccept=False
    )

    # Initialize keyboard and mouse:
    event.clearEvents(eventType='keyboard')
    key_response = event.BuilderKeyResponse()

    win.setMouseVisible(False)

    ScreenHZ = win.getActualFrameRate(nIdentical=60,
                                      nMaxFrames=100,
                                      nWarmUpFrames=10,
                                      threshold=1)

    ISI = core.StaticPeriod(screenHz=ScreenHZ, win=win)
    print("Frame Rate")
    print(ScreenHZ)

    process_priority = 'high'  # 'high' or 'realtime'

    if process_priority == 'normal':
        pass
    elif process_priority == 'high':
        core.rush(True)
    elif process_priority == 'realtime':
        # Only makes a diff compared to 'high' on Windows.
        core.rush(True, realtime=True)
    else:
        print 'Invalid process priority:',
        process_priority, "Process running at normal."
        process_priority = 'normal'

    # Create timers:
    routineTimer = core.CountdownTimer()
    routine_time = core.Clock()


# Define instructions intro ---------------------------------------------------
def instructions(start_num, end_num):
    prev_instr = start_num
    current_instr = start_num + 1

    event.clearEvents(eventType='keyboard')

    routine_time.reset()
    theseKeys = []
    continueRoutine = True

    # First instruction
    instruction_objects[start_num].setAutoDraw(True)
    win.flip()
    # print(buttons)

    while continueRoutine:
        # Next instruction
        theseKeys = event.getKeys(keyList=['space'])

        if current_instr <= end_num and len(theseKeys) > 0:
            instruction_objects[prev_instr].setAutoDraw(False)
            win.flip()
            ISI.start(0.5)
            instruction_objects[current_instr].setAutoDraw(True)
            arrow.setAutoDraw(True)
            current_instr += 1
            prev_instr += 1
            ISI.complete()
            theseKeys = []

        # End instructions
        if len(theseKeys) > 0 and current_instr > end_num:
            instruction_objects[prev_instr].setAutoDraw(False)
            arrow.setAutoDraw(False)
            ISI.start(0.5)
            continueRoutine = False
            ISI.complete()
            theseKeys = []
            win.flip()

        if continueRoutine:
            win.flip()

        if event.getKeys(keyList=["escape"]):
            core.quit()

# Fixation cross --------------------------------------------------------------


def fixation_cross():
    # Routine for the fixation cross
    global fixationCross
    continueRoutine = True
    cross_started = False
    delay_started = False
    t = 0
    routine_time.reset()  # clock
    routineTimer.reset()
    routineTimer.add(fxc_duration + fxc_delay)

    while continueRoutine:

        while routineTimer.getTime() > 0:

            t = routine_time.getTime()

            if t >= 0 and cross_started is False:
                cross_started = True
                fixationCross.setAutoDraw(True)

            elif t >= fxc_duration and delay_started is False:
                delay_started = True
                fixationCross.setAutoDraw(False)

            elif t >= (fxc_duration + fxc_delay):
                continueRoutine = False
                break

            # check for quit (the Esc key)
            if event.getKeys(keyList=["escape"]):
                core.quit()

            if continueRoutine:
                win.flip()
        break


# Main block ------------------------------------------------------------------


def main_block(n_trials):

    # run next_block() to set up next block
    # create an object of type KeyRespons:

    continueRoutine = True
    time_stamp = 0

    while continueRoutine:
        for trial in range(n_trials + 1):
            if trial == n_trials:
                continueRoutine = False
                break

            win.flip()
            ISI.start(isi)
            image_path = "images/conde/" + return_next_picture()

            # initialize current stimuli:
            stimuli = visual.ImageStim(
                win=win,
                name='stimuli',
                image=image_path,
                mask=None,
                ori=0,
                pos=[0, 0.2],
                size=pic_size,
                color=[1, 1, 1],
                colorSpace=u'rgb',
                opacity=1,
                flipHoriz=False,
                flipVert=False,
                interpolate=True)

            ISI.complete()

            fixation_cross()

            stimuli_started = False
            response_started = False
            press = False
            set_answer('.')
            set_reaction_time('.')
            set_scale('.')
            set_reaction_time_int('.')
            marker.setPos(newPos=[0.0, -0.75])
            rs.reset()
            event.clearEvents(eventType='keyboard')

            t = 0
            theseKeys = []
            routine_time.reset()  # clock
            routineTimer.add(stim_duration)

            while routineTimer.getTime() > 0:
                theseKeys = event.getKeys(keyList=['left', 'right'])
                stimuli_started = True
                stimuli.draw()
                beauty_question.draw()
                yes_response.draw()
                no_response.draw()
                t = routine_time.getTime()

                if t >= stim_duration and stimuli_started is True:
                    stimuli_started = False
                    event.clearEvents(eventType='Keyboard')
                    win.flip()

                if t < stim_duration and press is False and len(theseKeys) > 0:
                    reaction_time = t

                    if theseKeys == ['left']:
                        set_answer('1')
                        marker.setPos(newPos=[-0.1, -0.7])

                    elif theseKeys == ['right']:
                        set_answer('0')
                        marker.setPos(newPos=[0.1, -0.7])

                    marker.draw()
                    win.flip()
                    # ISI.start(0.5)
                    # ISI.complete()

                    if run_version == False:
                        set_reaction_time(str(reaction_time))
                        press = True
                        event.clearEvents(eventType='Keyboard')

                        while routineTimer.getTime() > 0 and press is True:
                            stimuli.draw()
                            sorrow_joy.draw()
                            rs.draw()
                            win.flip()
                            set_scale(rs.getRating())

                    elif run_version == True:
                        ISI.start(routineTimer.getTime())
                        set_reaction_time(str(reaction_time))
                        press = True
                        ISI.complete()
                        win.flip()

                if continueRoutine:
                    win.flip()
                # check for quit (the Esc key)
                if event.getKeys(keyList=["escape"]):
                    core.quit()
            time_stamp = routine_time.getTime()
            set_time_stamp(str(time_stamp))
            log_event()


def main_block_new(n_trials):

    # run next_block() to set up next block
    # create an object of type KeyRespons:

    continueRoutine = True
    time_stamp = 0

    while continueRoutine:
        for trial in range(n_trials + 1):
            if trial == n_trials:
                continueRoutine = False
                break

            win.flip()
            ISI.start(isi)
            image_path = "images/conde/" + return_next_picture()

            # initialize current stimuli:
            stimuli = visual.ImageStim(
                win=win,
                name='stimuli',
                image=image_path,
                mask=None,
                ori=0,
                pos=[0, 0.2],
                size=pic_size,
                color=[1, 1, 1],
                colorSpace=u'rgb',
                opacity=1,
                flipHoriz=False,
                flipVert=False,
                interpolate=True)

            ISI.complete()

            fixation_cross()

            stimuli_started = False
            response_started = False
            press = False
            set_answer('.')
            set_reaction_time('.')
            set_scale('.')
            set_reaction_time_int('.')
            marker.setPos(newPos=[0.0, -0.75])
            rs.reset()
            event.clearEvents(eventType='keyboard')

            t = 0
            theseKeys = []
            routine_time.reset()  # clock
            routineTimer.add(stim_duration)

            while press is False:
                theseKeys = event.getKeys(keyList=['left', 'right'])
                stimuli_started = True
                stimuli.draw()
                beauty_question.draw()
                yes_response.draw()
                no_response.draw()
                t = routine_time.getTime()

                if press is False and len(theseKeys) > 0:
                    reaction_time = t
                    if theseKeys == ['left']:
                        set_answer('1')
                        marker.setPos(newPos=[-0.1, -0.7])

                    elif theseKeys == ['right']:
                        set_answer('0')
                        marker.setPos(newPos=[0.1, -0.7])
                    press = True
                    marker.draw()
                    ISI.start(1)
                    # win.flip()

                if continueRoutine:
                    win.flip()
                # check for quit (the Esc key)
                if event.getKeys(keyList=["escape"]):
                    core.quit()
            time_stamp = routine_time.getTime()
            set_time_stamp(str(time_stamp))
            log_event()
            ISI.complete()


def run_training_text1():
    t = 0
    routine_time.reset()
    while t < 3:
        t = routine_time.getTime()
        training_text1.draw()
        win.flip()


def run_training_text2():
    t = 0
    routine_time.reset()
    while t < 3:
        t = routine_time.getTime()
        training_text2.draw()
        win.flip()


def training_block(n_trials):

    # run next_block() to set up next block
    # create an object of type KeyRespons:
    run_training_text1()

    n_trials = 5

    continueRoutine = True
    time_stamp = 0
    win.flip()
    while continueRoutine:
        for trial in range(n_trials + 1):
            if trial == n_trials:
                run_training_text2()
                continueRoutine = False
                break
            win.flip()
            ISI.start(isi)
            image_path = "images/training/" + return_next_picture()

            # initialize current stimuli:
            stimuli = visual.ImageStim(
                win=win,
                name='stimuli',
                image=image_path,
                mask=None,
                ori=0,
                pos=[0, 0.2],
                size=pic_size,
                color=[1, 1, 1],
                colorSpace=u'rgb',
                opacity=1,
                flipHoriz=False,
                flipVert=False,
                interpolate=False)

            ISI.complete()

            fixation_cross()

            stimuli_started = False
            response_started = False
            press = False
            # set_answer('.')
            # set_reaction_time('.')
            # set_valence('.')
            # set_scale('.')
            # set_reaction_time_int('.')
            marker.setPos(newPos=[0.0, -0.75])
            rs.reset()
            event.clearEvents(eventType='keyboard')

            t = 0
            theseKeys = []
            routine_time.reset()  # clock
            routineTimer.add(stim_duration)

            while routineTimer.getTime() > 0:
                theseKeys = event.getKeys(keyList=['left', 'right'])
                stimuli_started = True
                stimuli.draw()
                beauty_question.draw()
                yes_response.draw()
                no_response.draw()
                t = routine_time.getTime()

                if t >= stim_duration and stimuli_started is True:
                    stimuli_started = False
                    event.clearEvents(eventType='Keyboard')
                    win.flip()

                if t < stim_duration and press is False and len(theseKeys) > 0:
                    reaction_time = t

                    if theseKeys == ['left']:
                        # set_answer('1')
                        marker.setPos(newPos=[-0.1, -0.7])

                    elif theseKeys == ['right']:
                        # set_answer('0')
                        marker.setPos(newPos=[0.1, -0.7])

                    marker.draw()
                    win.flip()
                    # ISI.start(0.5)
                    # ISI.complete()

                    if run_version == False:
                        # set_reaction_time(str(reaction_time))
                        press = True
                        event.clearEvents(eventType='Keyboard')

                        while routineTimer.getTime() > 0 and press is True:
                            stimuli.draw()
                            sorrow_joy.draw()
                            rs.draw()
                            win.flip()
                            # set_scale(rs.getRating())

                    elif run_version == True:
                        ISI.start(routineTimer.getTime())
                        # set_reaction_time(str(reaction_time))
                        press = True
                        event.clearEvents(eventType='Keyboard')
                        ISI.complete()
                        win.flip()

                # check for quit (the Esc key)
                if event.getKeys(keyList=["escape"]):
                    core.quit()

                if continueRoutine:
                    win.flip()
            # time_stamp = routine_time.getTime()
            # set_time_stamp(str(time_stamp))
            # log_event()


# Run experiment --------------------------------------------------------------

def run_main_exp():
    # Block 1
    # kss.rating()
    next_block()
    main_block_new(n_trials)    # Experiment block 1

    # Block 2
    instructions(2, 2)      # Instructions(start, end) of list
    kss.rating()             # kss rating scale
    next_block()            # next block
    main_block(n_trials)    # Experiment block 2

    # Block 3
    instructions(2, 2)      # Instructions(start, end) of list
    kss.rating()              # kss rating scale
    next_block()            # next block
    main_block(n_trials)    # Experiment block 3

    # Block 4
    instructions(2, 2)      # Instructions(start, end) of list
    kss.rating()              # kss rating scale
    next_block()            # next block
    main_block(n_trials)    # Experiment block 4
    instructions(3, 3)      # Instructions(start, end) of list


def run_beauty_experiment():
    initialize_components()  # initialize components needed
    log_init(version, subject_id, load_set)  # create log file
    set_start_version(version)  # start version
    # if run_survey == True:
    # survey.run_survey_art()

    if run_training == True:
        instructions(0, 1)
        training_block(n_trials)
        instructions(1, 1)
        run_main_exp()

    elif run_training == False:
        instructions(0, 1)
        run_main_exp()


run_beauty_experiment()
win.close()
run_survey()
