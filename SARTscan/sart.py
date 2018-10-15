#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import core
import collections
import time
import instructions
import mylogging
import gui


# dialog box must be before importing psychopy visual and event, else crash
dlg = gui.GUI('SART')
expinfo = dlg.start()
print(expinfo)
# for testing
# expinfo = {'subject_id': 'test',
#            'expName': 'SART'}


class sart():

    def __init__(self,
                 screen_size=(1440, 900),
                 screen_color='black',
                 nTrials=560,
                 numTime=.250,
                 maskTime=.900,
                 fullscreen=False):

        self.trials = nTrials
        self.numTime = numTime
        self.maskTime = maskTime
        self.FullScreen = fullscreen
        self.screen_size = screen_size
        self.screen_color = screen_color
        self.mri_scan = expinfo['mri']
        self.globalClock = core.Clock()

    # Recieves MRI pulse, needed to sync timing with scanner
    def MRI(self):
        from psychopy.hardware.emulator import launchScan
        MR_settings = {
            'TR': 2.000,  # duration (sec) per volume
            'volumes': 210,  # number of whole-brain 3D volumes / frames
            'sync': 's',  # character to use as the sync timing event;
                          # assumed to come at start of a volume
            'skip': 0,  # number of volumes lacking a sync pulse at start of
                        # scan (for T1 stabilization)
            'sound': False,
            }
        launchScan(
            self.win, MR_settings,
            mode='Scan',  # also takes 'Test'
            globalClock=self.globalClock,
            log=False)

    # Create trial lists based on pre-defined lists on text-files
    def createTrials(self):
        # import trial lists
        if expinfo['version'] == '1':
            f = open('lists/list_1.txt', 'r')
        elif expinfo['version'] == '2':
            f = open('lists/list_2.txt', 'r')
        elif expinfo['version'] == '3':
            f = open('lists/list_3.txt', 'r')
        elif expinfo['version'] == '4':
            f = open('lists/list_4.txt', 'r')
        elif expinfo['version'] == '5':
            f = open('lists/list_5.txt', 'r')

        trials = f.read().split('\n')
        return trials

    # def createTrials(self):
        # For future, create a python randomizer

    # Create the trial list and assign what to be written on data file
    def experimentTrials(self, trials):
        # self.exp = expinfo
        self.trialList = []  # change to dict?
        for digit in trials:

            if digit == 3:
                type = 'NoGo'
            elif digit == 0:
                type = 'MW'
            else:
                type = 'Go'

            dataList = collections.OrderedDict()
            dataList['subject_id'] = expinfo['subject_id']
            dataList['Task'] = expinfo['expName']
            dataList['Version'] = expinfo['version']
            dataList['Date'] = time.strftime("%Y%m%d")
            dataList['Time'] = time.strftime("%H:%M:%S")
            dataList['GlobalTimeStamp'] = 0
            dataList['trialTimeStamp'] = 0
            dataList['Trial'] = 0
            dataList['Type'] = type
            dataList['Stimulus'] = digit
            dataList['Response'] = '0'
            dataList['RT'] = ''
            dataList['Accuracy'] = '0'
            dataList['multiResp'] = ''
            dataList['multiRT'] = ''
            dataList['dualWhereResp'] = ''
            dataList['dualWhereRT'] = ''
            dataList['dualAwareResp'] = ''
            dataList['dualAwareRT'] = ''

            self.trialList.append(dataList)

        return self.trialList

    # Create stimuli to show on screen, numbers and mask
    def createStim(self):
        from psychopy import visual

        stimuli = {}
        stimuli['number'] = visual.TextStim(self.win, text='', height=0.2)
        stimuli['mask'] = visual.SimpleImageStim(self.win,
                                                 image='stim/MaskCircle.png')
        return stimuli

    # Which response buttons to use
    def responseType(self):
        from psychopy import event
        if self.mri_scan:
            # According to Karolinska scanner
            resp = event.getKeys(keyList=['4', '3'])
        else:
            # If running on regular keyboard
            resp = event.getKeys(keyList=['a', 'l', 'space'])
        return resp

    # Define the trial loop
    def runTrials(self, trialObj):
        from psychopy import event
        import mindwandering
        self.mw = mindwandering.mwDual(self.win)
        self.trialhandler = trialObj
        self.countTrials = 0
        self.timer = core.Clock()
        stim = self.createStim()

        # Timing based on frames and frame rate
        self.targetFrames = int(self.frameR * self.numTime)
        self.itiFrames = int(self.frameR * self.maskTime)

        # Log file
        self.log.createFile(self.trialhandler[0])

        for trial in self.trialhandler:
            if trial['Stimulus'] == '0':
                mwResp = self.mw.rating()
                trial['Type'] = mwResp['Type']
                if mwResp['Type'] == 'MWdual':
                    trial['dualWhereResp'] = mwResp['Response where']
                    trial['dualAwareResp'] = mwResp['Response aware']
                    trial['dualWhereRT'] = mwResp['RT where']
                    trial['dualAwareRT'] = mwResp['RT aware']
                elif mwResp['Type'] == 'MWmulti':
                    trial['multiResp'] = mwResp['Response']
                    trial['multiRT'] = ['RT']
                # self.log.append(trial)

            else:
                stim['number'].setText(trial['Stimulus'])
                self.timer.reset()
                for frame in range(self.targetFrames):
                    stim['number'].draw()
                    self.win.flip()
                    trial['GlobalTimeStamp'] = self.globalClock.getTime()
                for frame in range(self.itiFrames):
                    response = self.responseType()
                    stim['mask'].draw()
                    self.win.flip()

                    if response:
                        trial['Response'] = '1'
                        trial['RT'] = self.timer.getTime()

                    if trial['Response'] == '1':
                        if trial['Type'] == 'Go':
                            trial['Accuracy'] = '1'
                        elif trial['Type'] == 'NoGo':
                            trial['Accuracy'] = '0'

                    elif trial['Response'] == '0':
                        if trial['Type'] == 'Go':
                            trial['Accuracy'] = '0'
                        elif trial['Type'] == 'NoGo':
                            trial['Accuracy'] = '1'

                self.countTrials += 1  # add 1 to count
            trial['trialTimeStamp'] = self.timer.getTime()
            trial['Time'] = time.strftime("%H:%M:%S")
            trial['Trial'] = self.countTrials
            self.log.append(trial)

            if event.getKeys(keyList=["escape"]):
                core.quit()

    # Import instructions
    def instructions(self):
        instr = instructions.instructions(self.win, text_size=0.09,
                                          key=['4', '3', 'space'])
        return instr

    # Import logging function
    def logging(self):
        log = mylogging.log()
        return log

    # Define window properties
    def expWindow(self):
        from psychopy import visual
        self.win = visual.Window(size=self.screen_size,
                                 fullscr=self.FullScreen,
                                 screen=0,
                                 allowGUI=False,
                                 allowStencil=False,
                                 monitor='testMonitor',
                                 color=self.screen_color,
                                 colorSpace='rgb',
                                 winType='pyglet')

        self.win.mouseVisable = False
        return self.win

    # Define experiment
    def startexp(self):
        self.win = self.expWindow()
        self.instr = self.instructions()
        self.frameR = self.win.getActualFrameRate()
        if not self.frameR:
            self.frameR = 60.0
        self.instr.start('intro1')
        self.trials = self.createTrials()
        trialsToRun = self.experimentTrials(self.trials)
        self.log = self.logging()
        if self.mri_scan:
            self.MRI()  # wait for MRI pulse
            print(self.globalClock.getTime())
        else:
            self.globalClock.reset()
        self.runTrials(trialsToRun)
        self.instr.start('end')


if expinfo != 'User pressed cancel':

    run = sart(fullscreen=True,
               screen_size=(1440, 900),
               screen_color='black',
               nTrials=560,
               numTime=.250,
               maskTime=.900
               )

    run.startexp()