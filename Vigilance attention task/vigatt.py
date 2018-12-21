#!/usr/bin/env/python
# -*- coding: utf-8 -*-
# noqa: F402

'''
Script by Andreas Gerhardson (2018.12.13)
'''
import random
import collections
import time
import sys

from psychopy import visual, core, event

import_from_misc = True

if import_from_misc is True:
    sys.path.append('..')
    from misc import gui, instructions, mylogging


class Vigilance():

    def __init__(self,
                 fullscreen=True,
                 winSize=(1280, 800),
                 bgCol='black',
                 textCol='white',
                 nTrials=40,
                 feedback=True,
                 dataFolder='data/'):

        self.fullscreen = fullscreen
        self.winSize = winSize
        self.bgCol = bgCol
        self.textCol = textCol
        self.nTrials = nTrials
        self.dataFolder = dataFolder
        self.feedback = feedback

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
        log = mylogging.log(self.dataFolder)
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
        stimuli['time'] = visual.TextStim(self.win,
                                          text='o',
                                          height=2,
                                          units="deg",
                                          color=self.textCol)
        stimuli['false'] = visual.TextStim(self.win,
                                           text='F',
                                           height=2,
                                           units="deg",
                                           color='red')

        return(stimuli)

    def genTriallist(self):
        trialList = {}
        trialList['side'] = []
        trialList['soa'] = []

        for i in range(0, self.nTrials):
            trialList['soa'].append(random.uniform(0.1, 5))
            trialList['side'].append(random.randrange(-1, 2, 2))

        return trialList

    def experimentTrials(self, trials):

        # trialList = []  # change to dict?
        for data in trials:

            dataDict = collections.OrderedDict()
            dataDict['subject_id'] = expinfo['subject_id']
            dataDict['session'] = expinfo['session']
            dataDict['version'] = expinfo['version']
            dataDict['task'] = expinfo['expName']
            dataDict['date'] = time.strftime('%Y%m%d')
            dataDict['time'] = time.strftime('%H:%M:%S')

            dataDict['soa'] = trials['soa']
            dataDict['trial'] = None
            dataDict['side'] = trials['side']
            dataDict['response'] = None
            dataDict['rt'] = None

        return dataDict

    def runTrials(self, trialObj):

        trial = 0
        for side, soa in zip(trialObj['side'], trialObj['soa']):
            eventTimer = core.CountdownTimer(soa)
            trial += 1
            response = {}
            falseAlarm = False
            response['response'] = None
            response['rt'] = None
            self.stim['probe'].setPos(newPos=[side*12, 0])

            while eventTimer.getTime() > 0:
                self.stim['cross'].draw()
                self.win.flip()
                if event.getKeys(keyList=['space']):
                    event.clearEvents()
                    self.stim['false'].draw()
                    self.win.flip()
                    core.wait(0.5)
                    falseAlarm = True
                    break
            self.timer.reset()
            while eventTimer.getTime() < 0 and falseAlarm is False:
                self.stim['probe'].draw()
                self.win.flip()
                if event.getKeys(keyList=['space']):
                    event.clearEvents()
                    response['response'] = 1
                    response['rt'] = self.timer.getTime()
                    if self.feedback:
                        self.stim['time'].setText(
                            format(response['rt'], '4.3f'))
                        self.stim['time'].draw()
                        self.win.flip()
                    core.wait(0.5)
                    break

                if event.getKeys(keyList=['escape']):
                    core.quit()

            self.ISI.start(0.1)
            self.data['trial'] = trial
            self.data['soa'] = soa
            self.data['side'] = side
            self.data['response'] = response['response']
            self.data['rt'] = response['rt']

            self.log.append(self.data)
            self.ISI.complete()
            self.win.flip()

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

        self.ISI = core.StaticPeriod(screenHz=self.frameR)

        instructions.start('intro')
        self.runTrials(self.trials)
        instructions.start('end')
        self.win.close()


# ============================================================================
info = gui.ExperimentInfo(expName='Vigilance attention')
vigilance = Vigilance()

expinfo = info.run()
vigilance.startexp()
