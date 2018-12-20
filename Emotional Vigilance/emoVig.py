#!/usr/bin/env/python
# -*- coding: utf-8 -*-
# noqa: F402

'''
Script by Andreas Gerhardson (2018.12.13)
'''

import collections
import time
import sys

from psychopy import visual, core, event

import_from_misc = True

if import_from_misc is True:
    sys.path.append('..')
    from misc import gui, instructions, mylogging


class DotProbe():

    def __init__(self,
                 fullscreen=True,
                 winSize=(1280, 800),
                 bgCol='black',
                 textCol='white',
                 nTrials=96,
                 imgSize=[16, 12],
                 dataFolder='data/',
                 imgTime=0.5,
                 fxTime=0.75,
                 dotMax=2.0,
                 dualResponse=True):

        self.fullscreen = fullscreen
        self.winSize = winSize
        self.bgCol = bgCol
        self.textCol = textCol
        self.nTrials = nTrials
        self.imgSize = imgSize
        self.dataFolder = dataFolder
        self.dualResp = dualResponse
        self.imgTime = imgTime
        self.fxTime = fxTime
        self.dotMax = dotMax

        self.timer = core.Clock()
        self.globalTime = core.Clock()

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
        stimuli['false'] = visual.TextStim(self.win,
                                           text='F',
                                           pos=(0.0, -1),
                                           height=2,
                                           units="deg",
                                           color='red')
        stimuli['imgEmo'] = visual.ImageStim(self.win,
                                             size=self.imgSize,
                                             pos=[0, 0],
                                             units='deg')
        stimuli['imgNeu'] = visual.ImageStim(self.win,
                                             size=self.imgSize,
                                             pos=[0, 0],
                                             units='deg')

        return(stimuli)

    def genTriallist(self):

        # Starting positive
        if expinfo['version'] == '01':
            f = open('lists/list_1.txt', 'r')
        # Starting negative
        elif expinfo['version'] == '02':
            f = open('lists/list_2.txt', 'r')
        # Starting positive
        elif expinfo['version'] == '03':
            f = open('lists/list_3.txt', 'r')
        # Starting negative
        elif expinfo['version'] == '04':
            f = open('lists/list_4.txt', 'r')

        # Shuffled lists
        elif expinfo['version'] == '05':
            f = open('lists/list_5.txt', 'r')
        elif expinfo['version'] == '06':
            f = open('lists/list_6.txt', 'r')

        list_of_lists = []
        for line in f:
            inner_list = [elt.strip() for elt in line.split('\t')]
            list_of_lists.append(inner_list)
        col_names = list_of_lists[0]
        by_cols = zip(*list_of_lists[1:])
        f.close()

        iapsDict = collections.OrderedDict()

        for i, col_names in enumerate(col_names):
            iapsDict[col_names] = by_cols[i]

        return iapsDict

    def experimentTrials(self, trials):

        dataDict = collections.OrderedDict()

        dataDict['subject_id'] = expinfo['subject_id']
        dataDict['version'] = expinfo['version']
        dataDict['session'] = expinfo['session']
        dataDict['task'] = expinfo['expName']
        dataDict['date'] = time.strftime('%Y%m%d')
        dataDict['time'] = time.strftime('%H:%M:%S')
        dataDict['timestamp'] = None

        for data in trials:
            dataDict[data] = None

        dataDict['response'] = None
        dataDict['rt'] = None

        return dataDict

    def runTrials(self, trialObj):

        fxFrames = int(self.frameR*(self.fxTime-0.1))
        dotMaxFrames = int(self.frameR*self.dotMax)
        imgFrames = int(self.frameR*self.imgTime)

        trial = 0
        self.globalTime.reset()
        for probe, soa, emo, neu, side, val, con in zip(
            trialObj['probe_side'],
            trialObj['soa'],
            trialObj['emo_jpg'],
            trialObj['neu_jpg'],
            trialObj['emo_side'],
            trialObj['valence'],
            trialObj['congruence']
                                    ):

            trial += 1
            response = {}
            response['response'] = None
            response['rt'] = None
            soaFrames = int(self.frameR*float(soa))
            self.stim['imgEmo'].setPos(newPos=[int(side)*12, 0.0])
            self.stim['imgNeu'].setPos(newPos=[int(side)*-12, 0.0])
            self.stim['probe'].setPos(newPos=[int(probe)*12, 0.0])
            self.stim['imgEmo'].setImage('images/' + emo)
            self.stim['imgNeu'].setImage('images/' + neu)
            self.stim['cross'].setColor(self.textCol)
            for frame in range(fxFrames):
                self.stim['cross'].setAutoDraw(True)
                self.win.flip()
            for frame in range(imgFrames):
                self.stim['imgEmo'].draw()
                self.stim['imgNeu'].draw()
                self.win.flip()

            self.win.flip()
            for frame in range(soaFrames):
                event.clearEvents()
                self.win.flip()

            self.timer.reset()
            for frame in range(dotMaxFrames):
                self.stim['probe'].draw()
                self.win.flip()
                if self.dualResp:
                    theseKeys = event.getKeys(keyList=['left', 'right'])
                    if 'left' in theseKeys:
                        response['response'] = -1
                        response['rt'] = self.timer.getTime()
                        core.wait(0.1)
                        self.win.flip()
                        break

                    if 'right' in theseKeys:
                        response['response'] = 1
                        response['rt'] = self.timer.getTime()
                        core.wait(0.1)
                        self.win.flip()
                        break
                elif not self.dualResp:
                    theseKeys = event.getKeys(keyList=['space'])
                    if 'space' in theseKeys:
                        response['response'] = 1
                        response['rt'] = self.timer.getTime()
                        core.wait(0.1)
                        self.win.flip()
                        break

                if event.getKeys(keyList=['escape']):
                    core.quit()

            self.ISI.start(0.1)
            self.data['soa'] = soa
            self.data['emo_side'] = side
            self.data['probe_side'] = probe
            self.data['trial'] = trial
            self.data['emo_jpg'] = emo
            self.data['neu_jpg'] = neu
            self.data['valence'] = val
            self.data['congruence'] = con
            self.data['timestamp'] = self.globalTime.getTime()
            self.data['response'] = response['response']
            self.data['rt'] = response['rt']

            self.log.append(self.data)
            self.ISI.complete()

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
        self.ISI = core.StaticPeriod(screenHz=self.frameR)

        instructions.start('intro')
        self.runTrials(self.trials)
        instructions.start('end')
        self.win.close()


# ============================================================================
info = gui.ExperimentInfo(expName='Dot-Probe')

dotProbe = DotProbe()

expinfo = info.run()
dotProbe.startexp()
