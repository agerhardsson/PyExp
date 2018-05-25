#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division
from psychopy import event, visual, core
import time

quest1 = (u'Välj det alternativ nedan som bäst beskriver din\n'
         u' upplevelse just nu (precis innan denna fråga).')

alt1 = u'1. Jag fokuserade på uppgiften.'
alt2 = u'2. Jag tänkte på hur jag presterade på uppgiften.'
alt3 = u'3. Jag tänkte inte på någonting.'
alt4 = u'4. Jag märkte att jag började tänka på annat medan jag gjorde uppgiften.'
alt5 = (u'5. Jag tänkte på andra saker under uppgiften\n'
        u'     men jag var inte medveten om det förrän jag blev frågad.')


class mindw_class():

    def __init__(self,
                 win,
                 textcol='white'):

        self.win=win
        self.left=-0.5
        self.top=0.2
        self.right=-0.5
        self.bottom=-0.2
        self.txsize=0.1
        self.textcol=textcol

        self.mouse = visual.CustomMouse(win=self.win,
                                   leftLimit=self.left,
                                   topLimit=self.top,
                                   rightLimit=self.right,
                                   bottomLimit=self.bottom,
                                   pointer=None,
                                   visible=False)

        self.mouse.pointer = visual.TextStim(win=self.win,
                                        text='O',
                                        color='black',
                                        height=self.txsize,
                                        alignHoriz='center',
                                        alignVert='center'
                                        )
        self.wait_stim = visual.TextStim(win=self.win,
                                    text=u'Vänta...',
                                    alignHoriz='center',
                                    height=0.06,
                                    wrapWidth=1.8,
                                    color=textcol)
        self.mindw_scale = []

        self.text = visual.TextStim(
            win=self.win,
            text=quest1,
            alignHoriz='left',
            pos=[self.right, self.top*1.6],
            height=0.06,
            wrapWidth=1.8,
            color=textcol)

        self.mindw_scale.append(self.text)


        self.text = visual.TextStim(
            win=self.win,
            text=alt1,
            alignHoriz='left',
            pos=[self.right, self.top],
            height=0.06,
            wrapWidth=1.8,
            color=textcol)

        self.mindw_scale.append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=alt2,
            alignHoriz='left',
            pos=[self.right, self.top-0.1],
            height=0.06,
            wrapWidth=1.8,
            color=textcol)

        self.mindw_scale.append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=alt3,
            alignHoriz='left',
            pos=[self.right, self.top-0.2],
            height=0.06,
            wrapWidth=1.8,
            color=textcol)

        self.mindw_scale.append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=alt4,
            alignHoriz='left',
            pos=[self.right, self.top-0.3],
            height=0.06,
            wrapWidth=1.8,
            color=textcol)

        self.mindw_scale.append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=alt5,
            alignHoriz='left',
            pos=[self.right, self.top-0.44],
            height=0.06,
            wrapWidth=1.8,
            color=textcol)

        self.mindw_scale.append(self.text)

        self.spot = visual.Circle(win=self.win,
                                  radius=0.035,
                                  lineColor=textcol,
                                  lineWidth=3)

        self.routine_time = core.Clock()

    def return_response(self):
        return [self.y, self.rt]

    def wait(self):
        self.wait_stim.draw()
        self.win.flip()
        core.wait(1.5)

    def mindw_rating(self):
        self.wait()
        event.clearEvents(eventType='keyboard')
        self.continueRoutine = True
        self.press = False
        self.y = '.'
        self.routine_time.reset()

        while self.continueRoutine is True and self.press is False:
            self.t = self.routine_time.getTime()
            self.mouse1, self.mouse2, self.mouse3 = self.mouse.getPressed()

            if not self.mouse1 and self.press is False:
                for a in range(0, len(self.mindw_scale)):
                    self.mindw_scale[a].draw()
                self.spot.setPos((self.mouse.getPos()[0]+0.01,
                                  round(self.mouse.getPos()[1], 1)))
                self.spot.draw()
                self.mouse.draw()
                self.win.flip()

            if self.mouse1 and self.press is False:
                self.y = str(abs(round(self.mouse.getPos()[1], 1)*10-3))
                self.rt = self.t
                self.press = True
                core.wait(1)
                self.win.flip()
                core.wait(1)

            if self.press is True:
                self.continueRoutine = False

            if event.getKeys(keyList=["escape"]):
                core.quit()

# --------------------- Example -----------------------------------------------
# win = visual.Window(
#     fullscr=True,
#     monitor='testMonitor',
#     allowGUI=None,
#     checkTiming=True,
#     color='black'
# )
# #
# # subject_id = 2
# mindw = mindw_class(win)
#
#
# # mindw.wait()
# mindw.mindw_rating()
# mindw_score = mindw.return_response()[0]
# mindw_rt = mindw.return_response()[1]
# print mindw_score
# print mindw_rt
