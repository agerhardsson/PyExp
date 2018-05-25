#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules --------------------------------------------------------------
from __future__ import division  # handy tool for division

from psychopy import visual, core, event, gui

from sleep_beauty_load import *

from sleep_beauty_log import *

from kss_query import *


# Settings --------------------------------------------------------------------

WinWidth = 1280
WinHeigth = 800
FullScreen = True
text_size = 0.07

# Fixation cross duration:
fxc_duration = 1.000000

# Fixation cross delay:
fxc_delay = 1.000000

# Stimuli duration time
stim_duration = 6.000000

# Inter stimuli interval
isi = 1.000000

# Number of trials
n_trials = 5

# Load log --------------------------------------------------------------------

# load occupied participants number:
load_participants()

# show information box:
while True:
    # Store info about the experiment session
    expName = u'Aesthetics'
    expInfo = {
        'participant': '',
        'version (1-4)': '1'
    }
    dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
    if dlg.OK is False:
        print('User pressed cancel')
        core.quit()  # user pressed cancel
    if (expInfo['participant'] == '' or
       expInfo['version (1-4)'] == ''):
        warning = gui.Dlg(title='Warning')
        warning.addText('A least one field is empty')
        warning.show()
    elif check_number(int(expInfo['participant'])) is False:
        warning = gui.Dlg(title='Warning')
        warning.addText('Participant already exist!')
        warning.show()
    elif (int(expInfo['version (1-4)']) > 4 or
          int(expInfo['version (1-4)']) < 1):
        warning = gui.Dlg(title='Warning')
        warning.addText('Not a valid version!')
        warning.show()
    else:
        break
# Save participant to textfile "participant.txt":
save_participant(expInfo['participant'])


# log
subject_id = expInfo['participant']
version = expInfo['version (1-4)']

# Save info about subject_id and version to the logging script:
set_subject_id(subject_id)
set_version(version)

# Set up window ---------------------------------------------------------------
win = visual.Window(
    size=(WinWidth, WinHeigth),
    fullscr=FullScreen,
    monitor='testMonitor',
    allowGUI=None,
    checkTiming=True
)


def initialize_components():
    global instruction_objects
    global text_size
    global fixationCross
    global key_response
    global routineTimer
    global routine_time
    global ISI

    # set cursor invisible:
    win.setMouseVisible(False)
    win.flip()

    # create an object of type KeyResponse
    key_response = event.BuilderKeyResponse()
    event.clearEvents(eventType='keyboard')

    # load instruction slide texts to a list:
    instruction_texts = load_instructions()

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

    # initialize fixationCross:
    fixationCross = visual.TextStim(
        win=win,
        ori=0,
        name='fxc',
        text='+',
        font='Arial',
        alignHoriz='center',
        pos=[0, 0],
        height=0.2,
        wrapWidth=1.8,
        color='white',
        colorSpace='rgb',
        opacity=1)

    # Initialize keyboard:
    key_response = event.BuilderKeyResponse()
    theseKeys = event.getKeys(keyList=['a', 'l'])
    event.clearEvents(eventType='keyboard')

    # Create static period
    ScreenHZ = win.getActualFrameRate(nIdentical=60,
                                      nMaxFrames=100,
                                      nWarmUpFrames=10,
                                      threshold=1)

    ISI = core.StaticPeriod(screenHz=ScreenHZ, win=win)
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
    win.setMouseVisible(False)

    routine_time.reset()
    continueRoutine = True

    # First instruction
    instruction_objects[start_num].setAutoDraw(True)
    win.flip()


    while continueRoutine is True:
        theseKeys = event.getKeys(keyList=['space'])

        # Next instruction
        if len(theseKeys) > 0 and current_instr <= end_num:
            instruction_objects[prev_instr].setAutoDraw(False)
            instruction_objects[current_instr].setAutoDraw(True)
            current_instr += 1
            prev_instr += 1
            theseKeys = []
            event.clearEvents(eventType='keyboard')

        # End instructions
        if len(theseKeys) > 0 and current_instr > end_num:
            instruction_objects[prev_instr].setAutoDraw(False)
            theseKeys = []
            event.clearEvents(eventType='keyboard')
            continueRoutine = False
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
    win.setMouseVisible(False)

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
                print("FC time: " + str(t))
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

    while continueRoutine:
        for trial in range(n_trials + 1):
            if trial == n_trials:
                continueRoutine = False
                break

            ISI.start(isi)

            image_path = "images/" + return_next_picture()
            # initialize current stimuli:
            stimuli = visual.ImageStim(
                win=win,
                name='stimuli',
                image=image_path,
                mask=None,
                ori=0, pos=[0, 0],
                size=[1.0, 1.1],
                color=[1, 1, 1],
                colorSpace=u'rgb',
                opacity=1,
                flipHoriz=False,
                flipVert=False,
                texRes=128,
                interpolate=False,
                depth=0.0)

            ISI.complete()

            fixation_cross()

            stimuli_started = False
            response_started = False
            keys = False
            set_answer('.')
            set_reaction_time('.')

            t = 0
            routine_time.reset()  # clock
            routineTimer.add(stim_duration + isi)
            win.setMouseVisible(False)

            while routineTimer.getTime() > 0 and routineTimer.getTime() > 0:
                theseKeys = event.getKeys(keyList=['a', 'l'])
                t = routine_time.getTime()

                if t >= 0 and stimuli_started is False:
                    stimuli_started = True
                    stimuli.setAutoDraw(True)
                    start_time = t

                if t >= stim_duration and response_started is False:
                    response_started = True
                    stimuli.setAutoDraw(False)
                    time_stamp = t - start_time
                    set_time_stamp(str(time_stamp))

                if t <= stim_duration and keys is False:

                    if len(theseKeys) > 0:
                        from_start = t
                        reaction_time = t - start_time
                        set_reaction_time(str(reaction_time))
                        set_answer(theseKeys)

                        keys = True
                        # reset keyboard event
                        event.clearEvents(eventType='Keyboard')

                # check for quit (the Esc key)
                if event.getKeys(keyList=["escape"]):
                    core.quit()
                if continueRoutine:
                    win.flip()
            log_event()


initialize_components()

log_init(version, subject_id)
# log_init_kss()

# stimuli_lists()
set_start_version(version)

instructions(0, 1)  # Instructions(start, end) of list
kss_rating()
main_block(n_trials)
next_block()
kss_rating()
main_block(n_trials)
instructions(2, 2)
next_block()
main_block(n_trials)
instructions(3, 3)
