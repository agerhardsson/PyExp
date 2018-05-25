#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division
from psychopy import event, visual, core
import time


pre_quest = u'Tänkte du på något annat än uppgiften?'
pre_choice = (u'Ja = Vänster musknapp\n'
              u'Nej = Höger musknapp')
alt1 = u'2. Jag tänkte på hur jag presterade på uppgiften.'
alt2 = u'3. Jag tänkte inte på någonting.'
alt3 = u'4. Jag tänkte på den tidigare uppgiften.'
alt4 = u'5. Jag märkte att jag började tänka på annat medan jag gjorde uppgiften'
alt5 = (u'6. Jag tänkte på andra saker under uppgiften\n'
        u'    men jag var inte medveten om det förrän jag blev frågad.')


class mindw_class():

    def __init__(self,
                 win,
                 textcol='white'):

        self.win=win
        self.left=-0.5
        self.top=0.3
        self.right=-0.5
        self.bottom=-0.1
        self.txsize=0.1
        self.textcol=textcol

        self.ScreenHZ = self.win.getActualFrameRate(nIdentical=60,
                                          nMaxFrames=100,
                                          nWarmUpFrames=10,
                                          threshold=1)

        self.ISI = core.StaticPeriod(screenHz=self.ScreenHZ, win=win)

        self.mouse = visual.CustomMouse(win=self.win,
                                        leftLimit=self.left,
                                        topLimit=self.top,
                                        rightLimit=self.right,
                                        bottomLimit=self.bottom,
                                        clickOnUp=True,
                                        pointer=None,
                                        visible=False)

        self.mouse.pointer = visual.TextStim(win=self.win,
                                             text='O',
                                             color='black',
                                             height=self.txsize,
                                             alignHoriz='center',
                                             alignVert='center')

        self.clickmouse = event.Mouse(win=self.win,
                                      visible=False)

        self.mindw_quest = visual.TextStim(win=self.win,
                                           text=pre_quest,
                                           alignHoriz='center',
                                           pos=[0, 0],
                                           height=0.06,
                                           wrapWidth=1.8,
                                           color=textcol)
        self.mindw_choice = visual.TextStim(win=self.win,
                                            text=pre_choice,
                                            alignHoriz='center',
                                            pos=[0, -0.3],
                                            height=0.06,
                                            wrapWidth=1.8,
                                            color=textcol)

        self.mindw_scale = []
        self.text = visual.TextStim(win=self.win,
                                    text=alt1,
                                    alignHoriz='left',
                                    pos=[self.right, self.top],
                                    height=0.06,
                                    wrapWidth=1.8,
                                    color=textcol)

        self.mindw_scale.append(self.text)

        self.text = visual.TextStim(win=self.win,
                                    text=alt2,
                                    alignHoriz='left',
                                    pos=[self.right, self.top-0.1],
                                    height=0.06,
                                    wrapWidth=1.8,
                                    color=textcol)

        self.mindw_scale.append(self.text)

        self.text = visual.TextStim(win=self.win,
                                    text=alt3,
                                    alignHoriz='left',
                                    pos=[self.right, self.top-0.2],
                                    height=0.06,
                                    wrapWidth=1.8,
                                    color=textcol)

        self.mindw_scale.append(self.text)

        self.text = visual.TextStim(win=self.win,
                                    text=alt4,
                                    alignHoriz='left',
                                    pos=[self.right, self.top-0.3],
                                    height=0.06,
                                    wrapWidth=1.8,
                                    color=textcol)

        self.mindw_scale.append(self.text)

        self.text = visual.TextStim(win=self.win,
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
        return [self.yes, self.no, self.resp, self.rt]

    def mindw_rating1(self):
        event.clearEvents(eventType='keyboard')
        self.continueRoutine = True
        self.press = False
        self.yes = '0'
        self.no = '0'
        self.routine_time.reset()

        self.mindw_quest.draw()
        self.win.flip()

        while self.continueRoutine:
            self.t = self.routine_time.getTime()
            self.buttons = self.mouse.getPressed()
            if self.t > 1.5:
                self.mindw_quest.draw()
                self.mindw_choice.draw()
                self.win.flip()
                self.response = True

                if self.buttons[2] and self.response is True:
                    self.win.flip()
                    self.ISI.start(1)
                    self.no = '1'
                    self.clickmouse.clickReset()
                    self.press = False
                    self.ISI.complete()
                    break

                elif self.buttons[0] and self.response is True:
                    self.win.flip()
                    self.ISI.start(1)
                    self.yes = '1'
                    self.clickmouse.clickReset()
                    self.press = True
                    self.ISI.complete()
                    break

                if event.getKeys(keyList=["escape"]):
                    core.quit()

        if event.getKeys(keyList=["escape"]):
            core.quit()

    def mindw_rating2(self):
        event.clearEvents(eventType='keyboard')
        self.continueRoutine = True
        self.resp = '.'
        self.rt = '.'
        self.press2 = False
        self.routine_time.reset()

        while self.continueRoutine is True and self.press is True:
            self.t = self.routine_time.getTime()
            self.buttons = self.mouse.getPressed()

            for a in range(0, len(self.mindw_scale)):
                self.mindw_scale[a].draw()
            self.spot.setPos((self.mouse.getPos()[0]+0.01,
                              round(self.mouse.getPos()[1], 1)))
            self.spot.draw()
            self.mouse.draw()
            self.win.flip()


            if self.buttons[0]:
                self.resp = str(abs(round(self.mouse.getPos()[1], 1)*10-5))
                self.rt = self.t
                self.press2 = True
                core.wait(1.5)
                break

            if self.press2 is True:
                self.continueRoutine = False

            if event.getKeys(keyList=["escape"]):
                core.quit()


# --------------------- Example -----------------------------------------------
win = visual.Window(
    fullscr=False,
    monitor='testMonitor',
    allowGUI=None,
    checkTiming=True,
    color='black'
)
#
# subject_id = 2
mindw = mindw_class(win)

mindw.mindw_rating1()
mindw.mindw_rating2()
mindw_yes = mindw.return_response()[0]
mindw_no = mindw.return_response()[1]
mindw_resp = mindw.return_response()[2]
mindw_rt = mindw.return_response()[3]
print mindw_yes
print mindw_no
print mindw_resp
print mindw_rt
