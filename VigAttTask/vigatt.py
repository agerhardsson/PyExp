#!/usr/bin/env/python
# -*- coding: utf-8 -*-

'''
Script by Andreas Gerhardson (2018.12.13)
'''

import random
import collections
import time
from psychopy import visual, core, event
import instructions
import mylogging
import gui


class Vigilance():

    def __init__(self,
                 fullscreen=True,
                 winSize=(1280, 800),
                 bgCol='black',
                 textCol='white',
                 nTrials=40):

        self.fullscreen = fullscreen
        self.winSize = winSize
        self.bgCol = bgCol
        self.textCol = textCol
        self.nTrials = nTrials

        self.timer = core.Clock()

    def expWindow(self):
        self.win = visual.Window(size=self.winSize,
                                 fullscr=self.fullscreen,
                                 screen=0,
                                 monitor='testMonitor',
                                 color=self.bgCol,
                                 colorSpace='rgb',
                                 winType='pyglet')
        self.win.mouseVisible = False
        return self.win

    def instructions(self):
        instr = instructions.instructions(self.win,
                                          color=self.textCol)
        return instr

    def logging(self):
        log = mylogging.log()
        return log

    def createStim(self):
        stimuli = {}
        stimuli['cross'] = visual.TextStim(self.win,
                                           text='+',
                                           height=2,
                                           units="deg",
                                           color=self.textCol)
        stimuli['probe'] = visual.TextStim(self.win,
                                           text='o',
                                           height=2,
                                           units="deg",
                                           color=self.textCol)
        stimuli['false'] = visual.TextStim(self.win,
                                           text='F',
                                           pos=(0.0, -1),
                                           height=2,
                                           units="deg",
                                           color='red')

        return(stimuli)

    def genTriallist(self):
        trialList = {}
        trialList['side'] = []
        trialList['soa'] = []

        for i in range(0, self.nTrials):
            trialList['soa'].append(random.uniform(0.2, 5))
            trialList['side'].append(random.randrange(-1, 2, 2))

        return trialList

    def experimentTrials(self, trials):

        # trialList = []  # change to dict?
        for data in trials:

            dataDict = collections.OrderedDict()
            dataDict['subject_id'] = expinfo['subject_id']
            dataDict['Session'] = expinfo['session']
            dataDict['Task'] = expinfo['expName']
            dataDict['Version'] = expinfo['version']
            dataDict['Date'] = time.strftime('%Y%m%d')
            dataDict['Time'] = time.strftime('%H:%M:%S')

            dataDict['soa'] = trials['soa']
            dataDict['Trial'] = None
            dataDict['side'] = trials['side']
            dataDict['Response'] = None
            dataDict['RT'] = None

        return dataDict

    def runTrials(self, trialObj):

        trial = 0
        for side, soa in zip(trialObj['side'], trialObj['soa']):
            eventTimer = core.CountdownTimer(soa)
            trial += 1
            response = {}
            falseAlarm = False
            response['Response'] = None
            response['RT'] = None
            self.stim['cross'].setColor(self.textCol)
            self.stim['cross'].setAutoDraw(True)
            self.win.flip()
            self.stim['probe'].setPos(newPos=[side*12, 0])

            while eventTimer.getTime() > 0:
                if event.getKeys(keyList=['space']):
                    self.stim['cross'].setColor('red')
                    self.win.flip()
                    core.wait(0.1)
                    falseAlarm = True
                    break
            self.timer.reset()
            while eventTimer.getTime() < 0 and falseAlarm is False:
                self.stim['probe'].draw()
                self.win.flip()
                if event.getKeys(keyList=['space']):
                    response['Response'] = 1
                    response['RT'] = self.timer.getTime()
                    self.win.flip()
                    break

                if event.getKeys(keyList=['escape']):
                    core.quit()

            self.data['Trial'] = trial
            self.data['soa'] = soa
            self.data['side'] = side
            self.data['Response'] = response['Response']
            self.data['RT'] = response['RT']

            self.log.append(self.data)
            # print(self.data)
        self.stim['cross'].setAutoDraw(False)

    def startexp(self):
        self.win = self.expWindow()
        instructions = self.instructions()
        self.log = self.logging()
        self.trials = self.genTriallist()
        self.data = self.experimentTrials(self.trials)
        self.stim = self.createStim()

        # Log file
        self.log.createFile(self.data)

        self.frameR = self.win.getActualFrameRate()
        if not self.frameR:
            self.frameR = 60.0

        instructions.start('intro')
        self.runTrials(self.trials)
        instructions.start('end')
        self.win.close()


info = gui.ExperimentInfo()
expinfo = info.run()

run = Vigilance()

run.startexp()
