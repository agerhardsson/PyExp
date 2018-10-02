#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import core
from random import shuffle, sample
import collections
import time
import instructions
import mylogging
import gui


# dialog box must be before importing psychopy visual and event
dlg = gui.GUI('SART')
expinfo = dlg.start()
# for testing
# expinfo = {'subject_id': 'test',
#            'expName': 'SART'}


class sart():

    def __init__(self,
                 digits=16,
                 nTrials=225,
                 numTime=.250,
                 maskTime=.900,
                 fullscreen=False):

        self.digits = sample([1, 2, 4, 5, 6, 7, 8, 9, 1, 2, 4, 5, 6, 7, 8, 9],
                             digits-1)
        self.digits.append(3)
        self.nDigits = digits
        self.trials = nTrials
        self.numTime = numTime
        self.maskTime = maskTime
        self.FullScreen = fullscreen
        self.globalClock = core.Clock()

    def MRI(self):
        from psychopy.hardware.emulator import launchScan
        MR_settings = {
            'TR': 2.000,  # duration (sec) per volume
            'volumes': 210,  # number of whole-brain 3D volumes / frames
            'sync': 't',  # character to use as the sync timing event;
                          # assumed to come at start of a volume
            'skip': 4,  # number of volumes lacking a sync pulse at start of
                        # scan (for T1 stabilization)
            'sound': False,
            }
        launchScan(
            self.win, MR_settings,
            mode=expinfo['mode'],
            globalClock=self.globalClock,
            log=False)

    # def triggerIN(self):
    #     # future function to send a trigger
    #        StimTracker


    def createTrials(self):
        trials = []
        for trialSequence in range(self.trials//self.nDigits):
            shuffled = self.digits[:]
            shuffle(shuffled)
            trials.append(shuffled)
        return trials

    def experimentTrials(self, trials):
        # self.exp = expinfo
        self.trialList = []  # change to dict?

        for trialSequence in trials:
            for trial, digit in enumerate(trialSequence):
                trial += 1

                if digit != 3:
                    type = 'Go'
                else:
                    type = 'NoGo'

                dataList = collections.OrderedDict()
                dataList['subject_id'] = expinfo['subject_id']
                dataList['Task'] = expinfo['expName']
                dataList['Date'] = time.strftime("%Y%m%d")
                dataList['Time'] = time.strftime("%H:%M:%S")
                dataList['GlobalTimeStamp'] = 0
                dataList['trialTimeStamp'] = 0
                # dataList['GlobalTime'] = self.globalClock.getTime()
                dataList['Trial'] = 0
                dataList['Type'] = type
                dataList['Stimulus'] = digit
                dataList['Response'] = 0
                dataList['RT'] = 0
                dataList['Accuracy'] = 0

                self.trialList.append(dataList)

        return self.trialList

    def createStim(self):
        from psychopy import visual

        stimuli = {}
        stimuli['number'] = visual.TextStim(self.win, text='')
        stimuli['mask'] = visual.SimpleImageStim(self.win,
                                                 image='stim/MaskCircle.png')
        return stimuli

    def responseType(self):
        from psychopy import event
        resp = event.getKeys(keyList=['space'])
        return resp

    def mindwandering(self):
        import mindwandering
        atProbesList = [20, 40, 80, 100, 120, 140, 160, 180, 200, 220]
        self.mw = mindwandering.mw(self.win)
        return atProbesList

    def runTrials(self, trialObj):
        from psychopy import event
        self.trialhandler = trialObj
        self.countTrials = 0
        self.timer = core.Clock()
        stim = self.createStim()
        self.targetFrames = int(self.frameR * self.numTime)
        self.itiFrames = int(self.frameR * self.maskTime)
        self.log.createFile(self.trialhandler[0])
        self.mwProbeList = self.mindwandering()
        core.wait(1.0)

        for trial in self.trialhandler:
            stim['number'].setText(trial['Stimulus'])
            self.timer.reset()
            # stim['number'].setSize() vary size??????????????????

            for frame in range(self.targetFrames):
                stim['number'].draw()
                self.win.flip()
                trial['GlobalTimeStamp'] = self.globalClock.getTime()
            for frame in range(self.itiFrames):
                response = self.responseType()
                stim['mask'].draw()
                self.win.flip()

                if response:
                    # event.clearEvents()
                    trial['RT'] = self.timer.getTime()
                    trial['Response'] = 1
                    if trial['Type'] == 'Go':
                        trial['Accuracy'] = 1
                    elif trial['Type'] == 'NoGo':
                        trial['Accuracy'] = 0
                elif not response and trial['Type'] == 'NoGo':
                    trial['Accuracy'] = 1
            self.countTrials += 1  # add 1 to count
            trial['trialTimeStamp'] = self.timer.getTime()
            trial['Time'] = time.strftime("%H:%M:%S")
            trial['Trial'] = self.countTrials
            self.log.append(trial)

            if any(probe == self.countTrials for probe in self.mwProbeList):
                mwResp = self.mw.rating()
                trial['Response'] = mwResp['Response']
                trial['RT'] = mwResp['RT']
                trial['Type'] = 'mw'
                trial['Stimulus'] = 0
                self.log.append(trial)

            if event.getKeys(keyList=["escape"]):
                core.quit()

    def instructions(self):
        instr = instructions.instructions(self.win)
        return instr

    def logging(self):
        log = mylogging.log()
        return log

    def expWindow(self, size=(1280, 800), color='black'):
        from psychopy import visual
        self.win = visual.Window(size=size,
                                 fullscr=self.FullScreen,
                                 screen=0,
                                 allowGUI=False,
                                 allowStencil=False,
                                 monitor='testMonitor',
                                 color=color,
                                 colorSpace='rgb',
                                 winType='pyglet')

        self.win.mouseVisable = False
        return self.win

    def startexp(self):
        self.win = self.expWindow()
        self.instr = self.instructions()
        self.frameR = self.win.getActualFrameRate()
        if not self.frameR:
            self.frameR = 60.0
        # self.MRI()  # wait for MRI pulse
        print(self.globalClock.getTime())
        self.instr.start('intro1')
        self.trials = self.createTrials()
        trialsToRun = self.experimentTrials(self.trials)
        self.log = self.logging()
        self.runTrials(trialsToRun)


if expinfo != 'User pressed cancel':
    run = sart(fullscreen=True)
    run.startexp()
