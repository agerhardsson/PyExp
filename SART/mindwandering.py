#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from psychopy import event, visual, core

# Question and options for multi-response
quest1 = (u'Välj det alternativ nedan som bäst beskriver din\n'
          u' upplevelse just nu (precis innan denna fråga).')

alt1 = u'1. Jag fokuserade på uppgiften.'
alt2 = u'2. Jag tänkte på hur jag presterade på uppgiften.'
alt3 = u'3. Jag tänkte inte på någonting.'
alt4 = (u'4. Jag märkte att jag började tänka på annat medan '
        u'jag gjorde uppgiften.')
alt5 = (u'5. Jag tänkte på andra saker under uppgiften\n'
        u'     men jag var inte medveten om det förrän jag blev frågad.')

# Question and options for dual and likert response
quest2 = (u'Var fanns din uppmärksamhet precis innan denna fråga?')
resp2_1 = (u'På uppgiften')
resp2_2 = (u'Inte på uppgiften')

quest3 = (u'Hur medveten var du om var din uppmärksamhet fanns?')
resp3_1 = (u'Medveten')
resp3_2 = (u'Omedveten')

tLimit = 60


class mwMulti():

    def __init__(self,
                 win,
                 textcol='white'):

        self.win = win
        self.txsize = 0.1
        self.textcol = textcol

        self.pos = {}
        self.pos['left'] = -0.5
        self.pos['top'] = 0.2
        self.pos['right'] = -0.5
        self.pos['bottom'] = -0.2
        self.pos['quest'] = [self.pos['right'], self.pos['top']*1.6]
        self.pos['alt1'] = [self.pos['right'], self.pos['top']]
        self.pos['alt2'] = [self.pos['right'], self.pos['top']-0.1]
        self.pos['alt3'] = [self.pos['right'], self.pos['top']-0.2]
        self.pos['alt4'] = [self.pos['right'], self.pos['top']-0.3]
        self.pos['alt5'] = [self.pos['right'], self.pos['top']-0.44]
        self.pos['key1'] = [self.pos['right']+0.01, self.pos['top']]
        self.pos['key2'] = [self.pos['right']+0.01, self.pos['top']-0.1]
        self.pos['key3'] = [self.pos['right']+0.01, self.pos['top']-0.2]
        self.pos['key4'] = [self.pos['right']+0.01, self.pos['top']-0.3]
        self.pos['key5'] = [self.pos['right']+0.01, self.pos['top']-0.4]

        self.win.mouseVisable = False

    def createStim(self):

        stimuli = {}
        stimuli['mouse'] = visual.CustomMouse(
            win=self.win,
            leftLimit=self.pos['left'],
            topLimit=self.pos['top'],
            rightLimit=self.pos['right'],
            bottomLimit=self.pos['bottom'],
            pointer=None,
            visible=False)

        stimuli['spot'] = visual.Circle(
            win=self.win,
            radius=0.04,
            lineColor=self.textcol,
            lineWidth=3)

        stimuli['wait'] = visual.TextStim(
            win=self.win,
            text=u'Vänta...',
            alignHoriz='center',
            height=0.06,
            wrapWidth=1.8,
            color=self.textcol)

        stimuli['continue'] = visual.TextStim(
            win=self.win,
            text=u'Gör dig redo att fortsätta, flytta handen till MELLANSLAG',
            alignHoriz='center',
            height=0.06,
            wrapWidth=1.8,
            color=self.textcol)

        return stimuli

    def createScale(self):

        scale = []
        self.text = visual.TextStim(
            win=self.win,
            text=quest1,
            alignHoriz='left',
            pos=self.pos['quest'],
            height=0.06,
            wrapWidth=1.8,
            color=self.textcol)

        scale.append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=alt1,
            alignHoriz='left',
            pos=self.pos['alt1'],
            height=0.06,
            wrapWidth=1.8,
            color=self.textcol)

        scale.append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=alt2,
            alignHoriz='left',
            pos=self.pos['alt2'],
            height=0.06,
            wrapWidth=1.8,
            color=self.textcol)

        scale.append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=alt3,
            alignHoriz='left',
            pos=self.pos['alt3'],
            height=0.06,
            wrapWidth=1.8,
            color=self.textcol)

        scale.append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=alt4,
            alignHoriz='left',
            pos=self.pos['alt4'],
            height=0.06,
            wrapWidth=1.8,
            color=self.textcol)

        scale.append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=alt5,
            alignHoriz='left',
            pos=self.pos['alt5'],
            height=0.06,
            wrapWidth=1.8,
            color=self.textcol)

        scale.append(self.text)
        return scale

    def keyAnswer(self):
        if '1' in self.theseKeys or 'num_1' in self.theseKeys:
            keyResp = '1'
            self.stimuli['spot'].setPos(newPos=self.pos['key1'])
        elif '2' in self.theseKeys or 'num_2' in self.theseKeys:
            keyResp = '2'
            self.stimuli['spot'].setPos(newPos=self.pos['key2'])
        elif '3' in self.theseKeys or 'num_3' in self.theseKeys:
            keyResp = '3'
            self.stimuli['spot'].setPos(newPos=self.pos['key3'])
        elif '4' in self.theseKeys or 'num_4' in self.theseKeys:
            keyResp = '4'
            self.stimuli['spot'].setPos(newPos=self.pos['key4'])
        elif '5' in self.theseKeys or 'num_5' in self.theseKeys:
            keyResp = '5'
            self.stimuli['spot'].setPos(newPos=self.pos['key5'])
        # self.win.flip()
        return keyResp

    def rating(self):
        self.timer = core.Clock()
        self.stimuli = self.createStim()
        self.scale = self.createScale()

        self.stimuli['wait'].draw()
        self.win.flip()
        core.wait(1.5)

        response = {}
        response['Type'] = 'MWmulti'
        event.clearEvents(eventType='keyboard')
        self.timer.reset()

        while True:
            (self.mouse1,
             self.mouse2,
             self.mouse3) = self.stimuli['mouse'].getPressed()
            self.theseKeys = event.getKeys(keyList=['1', '2', '3', '4', '5',
                                                    'num_1', 'num_2',
                                                    'num_3', 'num_4', 'num_5'])

            for a in range(0, len(self.scale)):
                self.scale[a].setAutoDraw(True)

            self.stimuli['spot'].setPos((
                self.stimuli['mouse'].getPos()[0] + 0.01,
                round(self.stimuli['mouse'].getPos()[1], 1)))

            self.stimuli['spot'].draw()
            self.stimuli['mouse'].draw()
            self.win.flip()

            if self.mouse1:
                response['Response'] = str(abs(round(
                    self.stimuli['mouse'].getPos()[1], 1) * 10-3))
                response['RT'] = self.timer.getTime()
                core.wait(0.5)
                break

            elif self.theseKeys:
                response['Response'] = self.keyAnswer()
                response['RT'] = self.timer.getTime()
                self.stimuli['spot'].draw()
                self.win.flip()
                core.wait(1)
                break

            elif self.timer.getTime() > tLimit:
                response['Response'] = ''
                response['RT'] = self.timer.getTime()
                break

            if event.getKeys(keyList=["escape"]):
                core.quit()
        core.wait(0.5)
        for a in range(0, len(self.scale)):
            self.scale[a].setAutoDraw(False)
        self.win.flip()
        core.wait(0.2)

        self.stimuli['continue'].draw()
        self.win.flip()
        core.wait(1.5)
        return response


class mwDual():

    # Adapted from from Christoff et al., 2009. PNAS.

    # Original qustions
    # Where was your attention focused just before the probe?
    # On-task | Off-task

    # Svenska
    # Var fanns din uppmärksamhet precis innan denna fråga?
    # På uppgiften | Inte på uppgiften

    # Hur medveten var du om var din uppmärksamhet fanns?
    # Medveten | Inte medveten

    # How aware were you of where your attention was focused?
    # Aware | Unaware

    def __init__(self,
                 win,
                 text_size=0.15,
                 text_color='white'):

        self.win = win
        self.txsize = text_size
        self.textcol = text_color

        self.pos = {}
        self.pos['left'] = -0.45
        self.pos['top'] = -0.2
        self.pos['right'] = 0.45
        self.pos['bottom'] = -0.4
        self.pos['quest'] = [0.0, 0.2]
        self.pos['keyLeft'] = [self.pos['left'], self.pos['top']]
        self.pos['keyRight'] = [self.pos['right'], self.pos['top']]
        self.pos['markLeft'] = [self.pos['left'], self.pos['bottom']]
        self.pos['markRight'] = [self.pos['right'], self.pos['bottom']]

        self.win.mouseVisable = False

    def createScale(self):
        scale = {}
        scale['Attention where'] = []
        scale['Attention aware'] = []

        self.text = visual.TextStim(
            win=self.win,
            text=quest2,
            alignHoriz='center',
            pos=self.pos['quest'],
            height=self.txsize,
            wrapWidth=1.6,
            color=self.textcol)
        scale['Attention where'].append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=resp2_1,
            alignHoriz='center',
            pos=self.pos['keyLeft'],
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)
        scale['Attention where'].append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=resp2_2,
            alignHoriz='center',
            pos=self.pos['keyRight'],
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)
        scale['Attention where'].append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=quest3,
            alignHoriz='center',
            pos=self.pos['quest'],
            height=self.txsize,
            wrapWidth=1.6,
            color=self.textcol)
        scale['Attention aware'].append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=resp3_1,
            alignHoriz='center',
            pos=self.pos['keyLeft'],
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)
        scale['Attention aware'].append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=resp3_2,
            alignHoriz='center',
            pos=self.pos['keyRight'],
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)
        scale['Attention aware'].append(self.text)

        return scale

    def createStim(self):

        stimuli = {}
        stimuli['spot'] = visual.TextStim(
            win=self.win,
            text=u'X',
            alignHoriz='center',
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)

        stimuli['wait'] = visual.TextStim(
            win=self.win,
            text=u'Vänta...',
            alignHoriz='center',
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)

        stimuli['continue'] = visual.TextStim(
            win=self.win,
            text=u'Gör dig redo att fortsätta',
            alignHoriz='center',
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)

        return stimuli

    def keyAnswer(self):
        if '4' in self.theseKeys or 'a' in self.theseKeys:
            keyResp = '1'
            self.stimuli['spot'].setPos(newPos=self.pos['markLeft'])
        elif '3' in self.theseKeys or 'l' in self.theseKeys:
            keyResp = '0'
            self.stimuli['spot'].setPos(newPos=self.pos['markRight'])
        return keyResp

    def rating(self):
        self.timer = core.Clock()
        self.stimuli = self.createStim()
        self.scale = self.createScale()

        self.stimuli['wait'].draw()
        self.win.flip()
        core.wait(1.5)

        response = {}
        response['Type'] = 'MWdual'
        event.clearEvents(eventType='keyboard')
        self.timer.reset()

        while True:
            self.theseKeys = event.getKeys(keyList=['4', '3', 'l', 'a'])
            for a in range(0, 3):
                self.scale['Attention where'][a].setAutoDraw(True)
            self.win.flip()

            if self.theseKeys:
                response['Response where'] = self.keyAnswer()
                response['RT where'] = self.timer.getTime()
                self.stimuli['spot'].draw()
                self.win.flip()
                core.wait(0.5)
                break

            elif self.timer.getTime() > tLimit:
                response['Response where'] = ''
                response['RT where'] = self.timer.getTime()
                break

            if event.getKeys(keyList=["escape"]):
                core.quit()
        core.wait(0.5)
        for a in range(0, 3):
            self.scale['Attention where'][a].setAutoDraw(False)
        self.win.flip()
        core.wait(0.5)

        event.clearEvents(eventType='keyboard')
        self.timer.reset()

        while True:
            self.theseKeys = event.getKeys(keyList=['4', '3', 'l', 'a'])
            for a in range(0, 3):
                self.scale['Attention aware'][a].setAutoDraw(True)
            self.win.flip()

            if self.theseKeys:
                response['Response aware'] = self.keyAnswer()
                response['RT aware'] = self.timer.getTime()
                self.stimuli['spot'].draw()
                self.win.flip()
                core.wait(0.5)
                break

            elif self.timer.getTime() > tLimit:
                response['Response aware'] = ''
                response['RT aware'] = self.timer.getTime()
                break

            if event.getKeys(keyList=["escape"]):
                core.quit()
        core.wait(0.5)
        for a in range(0, 3):
            self.scale['Attention aware'][a].setAutoDraw(False)
        self.win.flip()
        core.wait(0.2)

        self.stimuli['continue'].draw()
        self.win.flip()
        core.wait(1.5)
        self.win.flip()
        core.wait(0.5)
        return response


class mwLikert():
    # TBC
    # Adapted from from Christoff et al., 2009. PNAS.

    # Original qustions
    # Where was your attention focused just before the probe?
    # On-task | Off-task

    # Svenska
    # Var fanns din uppmärksamhet precis innan denna fråga?
    # På uppgiften | Inte på uppgiften

    # Hur medveten var du om var din uppmärksamhet fanns?
    # Medveten | Inte medveten

    # How aware were you of where your attention was focused?
    # Aware | Unaware

    def __init__(self,
                 win,
                 text_size=0.15,
                 text_color='white'):

        self.win = win
        self.txsize = text_size
        self.textcol = text_color

        self.pos = {}
        self.pos['left'] = -0.45
        self.pos['top'] = -0.2
        self.pos['right'] = 0.45
        self.pos['bottom'] = -0.4
        self.pos['quest'] = [0.0, 0.2]
        self.pos['keyLeft'] = [self.pos['left'], self.pos['top']]
        self.pos['keyRight'] = [self.pos['right'], self.pos['top']]
        self.pos['markLeft'] = [self.pos['left']-.07, self.pos['bottom']]
        self.pos['markRight'] = [self.pos['right']+.07, self.pos['bottom']]

        self.win.mouseVisable = False

    def createScale(self):
        scale = {}
        scale['Attention where'] = []
        scale['Attention aware'] = []

        self.text = visual.TextStim(
            win=self.win,
            text=quest2,
            alignHoriz='center',
            pos=self.pos['quest'],
            height=self.txsize,
            wrapWidth=1.6,
            color=self.textcol)
        scale['Attention where'].append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=resp2_1,
            alignHoriz='center',
            pos=self.pos['keyLeft'],
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)
        scale['Attention where'].append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=resp2_2,
            alignHoriz='center',
            pos=self.pos['keyRight'],
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)
        scale['Attention where'].append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=quest3,
            alignHoriz='center',
            pos=self.pos['quest'],
            height=self.txsize,
            wrapWidth=1.6,
            color=self.textcol)
        scale['Attention aware'].append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=resp3_1,
            alignHoriz='center',
            pos=self.pos['keyLeft'],
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)
        scale['Attention aware'].append(self.text)

        self.text = visual.TextStim(
            win=self.win,
            text=resp3_2,
            alignHoriz='center',
            pos=self.pos['keyRight'],
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)
        scale['Attention aware'].append(self.text)

        scale['likert'] = visual.RatingScale(
            self.win,
            marker=self.stimuli['spot'],
            leftKeys=['a', '4'],
            rightKeys=['l', '3'],
            acceptKeys=['space', '2'],
            lineColor='Black',
            showValue=False,
            showAccept=False,
            markerColor='White',
            stretch=3,
            size=0.5,
            scale=None,
            labels=None,
            noMouse=True,
            markerStart=4
            )

        return scale

    def createStim(self):

        stimuli = {}
        stimuli['spot'] = visual.TextStim(
            win=self.win,
            text=u'X',
            alignHoriz='center',
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)

        stimuli['wait'] = visual.TextStim(
            win=self.win,
            text=u'Vänta...',
            alignHoriz='center',
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)

        stimuli['continue'] = visual.TextStim(
            win=self.win,
            text=u'Gör dig redo att fortsätta',
            alignHoriz='center',
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol)

        stimuli['arrowL'] = visual.TextStim(
            win=self.win,
            text=u'<',
            alignHoriz='center',
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol,
            pos=self.pos['markLeft']
            )

        stimuli['arrowR'] = visual.TextStim(
            win=self.win,
            text=u'>',
            alignHoriz='center',
            height=self.txsize,
            wrapWidth=1.8,
            color=self.textcol,
            pos=self.pos['markRight']
            )

        return stimuli

    def rating(self):
        self.timer = core.Clock()
        self.stimuli = self.createStim()
        self.scale = self.createScale()

        self.stimuli['wait'].draw()
        self.win.flip()
        core.wait(1.5)

        response = {}
        response['Type'] = 'MWLikert'
        self.timer.reset()
        while True:
            for a in range(0, 3):
                self.scale['Attention where'][a].draw()
            self.stimuli['arrowL'].draw()
            self.stimuli['arrowR'].draw()
            self.win.flip()
            self.scale['likert'].draw()
            if not self.scale['likert'].noResponse:
                response['Response where'] = self.scale['likert'].getRating()
                response['RT where'] = self.scale['likert'].getRT()
                break

            elif self.timer.getTime() > tLimit:
                response['Response where'] = ''
                response['RT where'] = self.timer.getTime()
                break

            if event.getKeys(keyList=["escape"]):
                core.quit()

        core.wait(0.2)
        self.win.flip()
        core.wait(0.2)

        self.scale['likert'].reset()
        self.timer.reset()
        while True:
            for a in range(0, 3):
                self.scale['Attention aware'][a].draw()
            self.stimuli['arrowL'].draw()
            self.stimuli['arrowR'].draw()
            self.win.flip()
            self.scale['likert'].draw()
            if not self.scale['likert'].noResponse:
                response['Response aware'] = self.scale['likert'].getRating()
                response['RT aware'] = self.scale['likert'].getRT()
                break

            elif self.timer.getTime() > tLimit:
                response['Response aware'] = ''
                response['RT aware'] = self.timer.getTime()
                break

            if event.getKeys(keyList=["escape"]):
                core.quit()

        core.wait(0.2)
        self.win.flip()
        core.wait(0.2)

        # self.stimuli['continue'].draw()
        # self.win.flip()
        # core.wait(1.5)
        return response


# Example --------------------------------------------------------------------
# win = visual.Window(
#     fullscr=False,
#     monitor=u'testMonitor',
#     allowGUI=None,
#     checkTiming=True,
#     color=u'black'
# )
#
# mindw = mwLikert(win)
#
# mwResp = mindw.rating()
# print(mwResp)
#
# mindw = mwDual(win)
#
# mwResp = mindw.rating()
# print(mwResp)
#
# mindw = mwMulti(win)
#
# mwResp = mindw.rating()
# print(mwResp)
