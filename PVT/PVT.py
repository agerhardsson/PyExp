#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules --------------------------------------------------------------
from __future__ import division  # handy tool for division

import random

from psychopy import visual, core, event

from pvt_log import *

from mindwandering import *
from kss_query import kss_class
import pvt_setup as setup

# run setup --------------------------------------------------------------------
setup.run_setup(useGui=True)

# log
subject_id = str(setup.participant)
max_time = setup.max_time * 60

# Save info about subject_id and version to the logging script:
set_subject_id(subject_id)
set_max_time(max_time)


# Settings --------------------------------------------------------------------

WinWidth = 400     # Set window Width
WinHeigth = 200     # Set window height
FullScreen = True  # Set full screen (True/False)
text_color = 'red'
num_color = 'red'
bg_color = 'black'
text_size = 0.07

# Mindwandering?
use_mindwandering = True  # True/False

# How many mindwandering interuptions?
max_runs = 7

# randomize the time between mindwandering, between 60 sek and time_run
time_run = max_time / (max_runs - 1)
episode_time = random.uniform(60, time_run)

if use_mindwandering == False:
    episode_time = max_time

# Version with clock counting = True, version with an appearing P = False
feedback = True

# Set up window ---------------------------------------------------------------
win = visual.Window(
    size=(WinWidth, WinHeigth),
    fullscr=FullScreen,
    monitor='testMonitor',
    allowGUI=None,
    checkTiming=True,
    color=bg_color
)

# -----------------------------------------------------------------------------

def initialise_components():
    global instruction_objects
    global text_size
    global mouse
    global buttons
    global routineTimer
    global clock
    global error_mess
    global ISI
    global clock_stim
    global trigger
    global mindw
    global trial
    global block
    global kss

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

    mindw = mindw_class(win)

    kss = kss_class(win=win,
                    textcol='white',
                    use_mouse=True,
                    subject_id=subject_id)

    # Initialise mouse
    mouse = event.Mouse(visible=False)
    buttons = mouse.getPressed()

    routineTimer = core.CountdownTimer()
    clock = core.Clock()

    error_mess = visual.TextStim(win,
                                 text="False",
                                 pos=(0, 0),
                                 color=text_color)

    trigger = visual.TextStim(win,
                                 text="P",
                                 pos=(0, 0),
                                 color=text_color)

    clock_stim = visual.TextStim(win,
                                 text=str(0.0)[:5],
                                 pos=(0.07, 0),
                                 alignHoriz='right',
                                 color=num_color)

    ScreenHZ = win.getActualFrameRate(nIdentical=60,
                                      nMaxFrames=100,
                                      nWarmUpFrames=10,
                                      threshold=1)

    ISI = core.StaticPeriod(screenHz=ScreenHZ, win=win)

    trial = 0
    block = 0


def instructions(start_num, end_num):
    prev_instr = start_num
    current_instr = start_num + 1

    event.clearEvents(eventType='keyboard')

    clock.reset()
    mouse.clickReset()
    continueRoutine = True

    # First instruction
    instruction_objects[start_num].setAutoDraw(True)
    win.flip()
    # print(buttons)

    while continueRoutine:
        # Next instruction
        buttons = mouse.getPressed()

        if current_instr <= end_num and buttons[0]:
            instruction_objects[prev_instr].setAutoDraw(False)
            win.flip()
            ISI.start(0.5)
            instruction_objects[current_instr].setAutoDraw(True)
            current_instr += 1
            prev_instr += 1
            ISI.complete()
            mouse.clickReset()

        # End instructions
        if buttons[0] and current_instr > end_num:
            instruction_objects[prev_instr].setAutoDraw(False)
            ISI.start(0.5)
            continueRoutine = False
            ISI.complete()
            mouse.clickReset()
            win.flip()

        if continueRoutine:
            win.flip()

        if event.getKeys(keyList=["escape"]):
            core.quit()


def run_kss():
    win.flip()
    kss.rating()
    set_reaction_time('.')


def run_mindwandering():
    mindw.mindw_rating()
    set_task('mw')
    set_mindw_answer(str(mindw.return_response()[0]))
    set_mindw_rt(str(mindw.return_response()[1]))
    log_event()


def exp_PVT(episode_time):
    global trial
    global block
    block = block + 1
    interval = random.uniform(0.2, 5)
    t = 0
    trial = trial + 1
    set_task('pvt')
    set_trial('.')
    set_interval('.')
    set_reaction_time('.')
    set_answer('0')
    set_mindw_answer('.')
    set_mindw_rt('.')
    continueRoutine = True
    count_start = False
    routineTimer.reset()
    routineTimer.add(episode_time)
    clock.reset()

    while continueRoutine and routineTimer.getTime() > 0:
        t = clock.getTime()

        if t < interval and buttons[0]:
            count_start = False
            error_mess.draw()
            win.flip()
            ISI.start(2)

            set_trial(str(trial))
            set_interval(str(interval))
            set_reaction_time(str(clock.getTime()))
            set_answer('0')
            log_event()

            interval = random.uniform(0.2, 5)
            trial = trial + 1

            mouse.clickReset()
            ISI.complete()
            clock.reset()
            win.flip()

        elif t > interval and not buttons[0]:
            count_start = True
            clock.reset()

            while count_start is True:
                count = clock.getTime()
                if count < 1:
                    clock_stim.setText(str(count * 1000)[:3])
                else:
                    clock_stim.setText(str(count * 1000)[:4])
                clock_stim.draw()
                win.flip()

                if buttons[0]:
                    reaction_time = str(count)
                    count_start = False
                    clock_stim.draw()
                    win.flip()
                    ISI.start(2)

                    set_trial(str(trial))
                    set_interval(str(interval))
                    set_reaction_time(str(count))
                    set_answer('1')
                    log_event()

                    mouse.clickReset()
                    interval = random.uniform(0.2, 5)
                    trial = trial + 1
                    ISI.complete()
                    clock.reset()
                    win.flip()
                    break
                if event.getKeys(keyList=["escape"]):
                    core.quit()

        if event.getKeys(keyList=["escape"]):
            core.quit()

def exp_PVT2(episode_time):
    global trial
    global block
    block = block + 1
    interval = random.uniform(0.2, 5)
    t = 0
    trial = trial + 1
    set_task('pvt_nofeeback')
    set_trial('.')
    set_interval('.')
    set_reaction_time('.')
    set_answer('0')
    set_mindw_answer('.')
    set_mindw_rt('.')
    continueRoutine = True
    count_start = False
    routineTimer.reset()
    routineTimer.add(episode_time)
    clock.reset()

    while continueRoutine and routineTimer.getTime() > 0:
        t = clock.getTime()

        if t < interval and buttons[0]:
            count_start = False
            error_mess.draw()
            win.flip()
            ISI.start(2)

            set_trial(str(trial))
            set_interval(str(interval))
            set_reaction_time(str(clock.getTime()))
            set_answer('0')
            log_event()

            interval = random.uniform(0.2, 5)
            trial = trial + 1

            mouse.clickReset()
            ISI.complete()
            clock.reset()
            win.flip()

        elif t > interval and not buttons[0]:
            count_start = True
            clock.reset()

            while count_start is True:
                trigger.draw()
                win.flip()
                count = clock.getTime()

                if buttons[0]:
                    reaction_time = str(count)
                    count_start = False
                    ISI.start(1)

                    set_trial(str(trial))
                    set_interval(str(interval))
                    set_reaction_time(str(count))
                    set_answer('1')
                    log_event()

                    mouse.clickReset()
                    interval = random.uniform(0.2, 5)
                    trial = trial + 1
                    ISI.complete()
                    clock.reset()
                    win.flip()
                    break
                if event.getKeys(keyList=["escape"]):
                    core.quit()

        if event.getKeys(keyList=["escape"]):
            core.quit()


def run_pvt():
    initialise_components()
    log_init(subject_id)  # create log file
    instructions(0, 0)  # instructions before task
    kss.rating()  # rate sleepiness

    exp_time = core.Clock()
    expTimer = core.CountdownTimer()
    exp_time.reset()
    expTimer.reset()

    runs = 1
    event_time = 0
    expTimer.add(max_time)

    while expTimer.getTime > 0:
        if runs > max_runs:
            break

        episode_time = random.uniform(1, time_run)
        if feedback == True:
            exp_PVT(episode_time)
        elif feedback == False:
            exp_PVT2(episode_time)

        if use_mindwandering is True:
            run_mindwandering()
            runs = runs + 1

    kss.rating()
    instructions(1, 1)


run_pvt()
