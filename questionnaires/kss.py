#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division
import time, os
from psychopy import event, visual, core

def kss(win, use_mouse=True, textcol='white'):

    win=win
    left=-0.5
    top=0.4
    right=-0.5
    bottom=-0.4
    txsize=0.1
    textcol=textcol
    use_mouse=use_mouse

# Create custom mouse for mouse selection ---------------------------------
    mouse = visual.CustomMouse(win=win,
                               leftLimit=left,
                               topLimit=top,
                               rightLimit=right,
                               bottomLimit=bottom,
                               pointer=None,
                               visible=False)

    mouse.pointer = visual.TextStim(win=win,
                                    text='O',
                                    color='black',
                                    height=txsize,
                                    alignHoriz='center',
                                    alignVert='center'
                                    )
# Create marker for selection ---------------------------------------------
    spot = visual.Circle(win=win,
                              radius=0.04,
                              lineColor=textcol,
                              lineWidth=3)
# create the kss scale ----------------------------------------------------
    kss_scale = []

    text = visual.TextStim(
        win=win,
        text=u'Hur sömnig har du känt dig under de senaste 5 minuterna?',
        alignHoriz='center',
        pos=[0, 0.7],
        height=0.08,
        wrapWidth=1.8,
        color=textcol)

    kss_scale.append(text)

    kss_alt = [
        u'1    Extremt pigg',
        u'2    Mycket pigg',
        u'3    Pigg',
        u'4    Ganska pigg',
        u'5    Varken pigg eller sömnig',
        u'6    Lätt sömnig',
        u'7    Sömnig men ej ansträngande vara vaken',
        u'8    Sömnig och något ansträngande att vara vaken',
        u'9    Mycket sömnig, mycket ansträngande att vara vaken,\n' +
             u'      kämpar mot sömnen',]
    kss_pos = top+0.1
    kss_set_pos = []

    for i in range(0, len(kss_alt)):

        text = visual.TextStim(
            win=win,
            text=kss_alt[i],
            alignHoriz='left',
            pos=[right, kss_pos],
            height=0.07,
            wrapWidth=1.8,
            color=textcol)

        if i < len(kss_alt)-1:
            kss_pos = kss_pos-0.1
        else:
            kss_pos = kss_pos-0.14  # last item needs two rows

        text.setPos(newPos=[right, kss_pos])
        kss_scale.append(text)
        kss_set_pos.append(kss_pos)

    routine_time = core.Clock()

# Run the rating scale ----------------------------------------------------
    event.clearEvents(eventType='keyboard')
    continueRoutine = True
    press = False
    routine_time.reset()
    kss_answer = '.'
    rt = '.'
    theseKeys = []

    while continueRoutine is True:
        t = routine_time.getTime()

        if use_mouse is True:
            mouse1, mouse2, mouse3 = mouse.getPressed()

            for a in range(0, len(kss_scale)):
                kss_scale[a].draw()
            spot.setPos((mouse.getPos()[0]+0.01,
                              round(mouse.getPos()[1], 1)))
            spot.draw()
            mouse.draw()
            win.flip()

            if mouse1 and press is False:
                kss_answer = str(abs(round(mouse.getPos()[1], 1)*10-5))
                rt = t
                press = True

        elif use_mouse is False:
            theseKeys = event.getKeys(
                keyList=['1', '2', '3', '4', '5', '6', '7', '8', '9',
                        'num_1', 'num_2', 'num_3','num_4', 'num_5',
                        'num_6', 'num_7', 'num_8', 'num_9'])

            for a in range(0, len(kss_scale)):
                kss_scale[a].draw()
            win.flip()

            if len(theseKeys) > 0 and press is False:
                if '1' in theseKeys or 'num_1' in theseKeys:
                    kss_answer = '1'
                    spot.setPos(newPos=[right+0.01, kss_set_pos[0]])
                elif '2' in theseKeys or 'num_2' in theseKeys:
                    kss_answer = '2'
                    spot.setPos(newPos=[right+0.01, kss_set_pos[1]])
                elif '3' in theseKeys or 'num_3' in theseKeys:
                    kss_answer = '3'
                    spot.setPos(newPos=[right+0.01, kss_set_pos[2]])
                elif '4' in theseKeys or 'num_4' in theseKeys:
                    kss_answer = '4'
                    spot.setPos(newPos=[right+0.01, kss_set_pos[3]])
                elif '5' in theseKeys or 'num_5' in theseKeys:
                    kss_answer = '5'
                    spot.setPos(newPos=[right+0.01, kss_set_pos[4]])
                elif '6' in theseKeys or 'num_6' in theseKeys:
                    kss_answer = '6'
                    spot.setPos(newPos=[right+0.01, kss_set_pos[5]])
                elif '7' in theseKeys or 'num_7' in theseKeys:
                    kss_answer = '7'
                    spot.setPos(newPos=[right+0.01, kss_set_pos[6]])
                elif '8' in theseKeys or 'num_8' in theseKeys:
                    kss_answer = '8'
                    spot.setPos(newPos=[right+0.01, kss_set_pos[7]])
                elif '9' in theseKeys or 'num_9' in theseKeys:
                    kss_answer = '9'
                    spot.setPos(newPos=[right+0.01, kss_set_pos[8]+0.04])

                rt = t

                for a in range(0, len(kss_scale)):
                    kss_scale[a].draw()
                spot.draw()
                win.flip()

                press = True

        if press is True:
            # set answers and position of marker according to answer ------------------


            kss_rt = str(rt)
            core.wait(1.5)
            win.flip()
            continueRoutine = False

        if event.getKeys(keyList=["escape"]):
            core.quit()

    response = {'kss': kss_answer, 'rt': kss_rt}
    return response
# --------------------- Example -----------------------------------------------
# win = visual.Window(fullscr=False, color='black')
#
# kss = kss(win, textcol='white', use_mouse=True)
