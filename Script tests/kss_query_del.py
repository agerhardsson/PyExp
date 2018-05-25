#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from psychopy import event, visual, core
import time

routineTimer = core.CountdownTimer()
routine_time = core.Clock()

# def set_subject_id(in_subject_id):
#     global subject_id
#     subject_id = in_subject_id
#
#
# def set_version(in_version):
#     global version
#     version = in_version
#
#
# def set_reaction_time(in_time):
#     global reaction_time
#     reaction_time = str(in_time)


def log_init_kss():
    global log_file_path
    log_file_path = "data/" + subject_id + "_kss.txt"
    f = open(log_file_path, "w")

    # write required parameters to columns in log file:
    f.write(
        'subject_id\t'
        + 'version\t'
        + 'date\t'
        + 'time\t'
        + 'kss_answer\t'
        + 'reaction_time\n'
    )

    f.close()


def set_kss(theseKeys):
    global kss_answer
    if '1' in theseKeys:
        kss_answer = '1'
    elif '2' in theseKeys:
        kss_answer = '2'
    elif '3' in theseKeys:
        kss_answer = '3'
    elif '4' in theseKeys:
        kss_answer = '4'
    elif '5' in theseKeys:
        kss_answer = '5'
    elif '6' in theseKeys:
        kss_answer = '6'
    elif '7' in theseKeys:
        kss_answer = '7'
    elif '8' in theseKeys:
        kss_answer = '8'
    elif '9' in theseKeys:
        kss_answer = '9'
    else:
        kss_answer = '.'


def log_kss():
    global log_file_path
    global subject_id
    global version
    global reaction_time
    global kss_answer

    log_init_kss()

    f = open(log_file_path, "a")
    f.write(
        subject_id + '\t'  # id
        + version + '\t'  # version
        + time.strftime("%d/%m/%Y") + '\t'  # date
        + time.strftime("%H:%M:%S") + '\t'  # time
        + kss_answer + '\t'  # kss answer
        + reaction_time + '\n'  # reaction time
    )
    f.close()


def kss_rating():
    # Routine for kss
    win = visual.Window(
        fullscr=True,
        monitor='testMonitor',
        allowGUI=None,
        checkTiming=True
    )

    event.clearEvents(eventType='keyboard')
    win.setMouseVisible(False)

    set_reaction_time('.')


    kss_scale = visual.TextStim(
        win=win,
        ori=0,
        name='kss_choices',
        text=u'1 - Extremt pigg\n' +
             u'2 - Mycket pigg\n' +
             u'3 - Pigg\n' +
             u'4 - Ganska pigg\n' +
             u'5 - Varken pigg eller sömnig\n' +
             u'6 - Lätt sömnig\n' +
             u'7 - Sömnig men ej ansträngande vara vaken\n' +
             u'8 - Sömnig och något ansträngande att vara vaken\n' +
             u'9 - Mycket sömnig, mycket ansträngande att vara vaken, \n' +
             u'     kämpar mot sömnen\n',
        font='Arial',
        alignHoriz='center',
        pos=[0, 0],
        height=0.07,
        wrapWidth=1.8,
        color='white',
        colorSpace='rgb',
        opacity=1)

    continueRoutine = True
    t = 0
    routine_time.reset()  # clock

    # scale
    kss_scale.setAutoDraw(True)
    win.flip()

    while continueRoutine is True:
        theseKeys = event.getKeys(keyList=['1', '2', '3',
                                           '4', '5', '6',
                                           '7', '8', '9'])
        t = routine_time.getTime()
        if len(theseKeys) > 0:
            reaction_time = t
            set_reaction_time(str(reaction_time))
            set_kss(theseKeys)
            kss_scale.setAutoDraw(False)
            theseKeys = []
            event.clearEvents(eventType='keyboard')
            continueRoutine = False
            win.flip()

        if continueRoutine:
            win.flip()

        if event.getKeys(keyList=["escape"]):
            core.quit()
    log_kss()
