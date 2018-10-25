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
        self.ntrials = nTrials
        self.training = False
        if expinfo['version'] == u'tr':
            self.ntrials = 47
            self.training = True
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
            mode=u'Scan',  # also takes 'Test'
            globalClock=self.globalClock,
            log=False)

    # Create trial lists based on pre-defined lists on text-files
    def createTrials(self):
        # import trial lists
        if expinfo['version'] == '01':
            f = open('lists/list_5.txt', 'r')
        elif expinfo['version'] == '02':
            f = open('lists/list_6.txt', 'r')
        elif expinfo['version'] == u'tr':
            f = open('lists/list_training.txt', 'r')

        expinfo['list'] = f.name[6:]
        trials = f.read().split('\n')
        return trials[0:self.ntrials]

    # def createTrials(self):
        # For future, create a python randomizer

    # Create the trial list and assign what to be written on data file
    def experimentTrials(self, trials):
        # self.exp = expinfo
        self.trialList = []  # change to dict?
        for digit in trials:

            if digit == '3':
                type = 'NoGo'
            elif digit == '0':
                type = 'MW'
            else:
                type = 'Go'

            dataList = collections.OrderedDict()
            dataList['subject_id'] = expinfo['subject_id'][:4]
            dataList['Session'] = expinfo['session']
            dataList['Task'] = expinfo['expName']
            dataList['Version'] = expinfo['version']
            dataList['list'] = expinfo['list']
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
        stimuli['number'] = visual.TextStim(
            self.win,
            text='',
            height=0.2)
        stimuli['mask'] = visual.SimpleImageStim(
            self.win,
            image='stim/MaskCircle125.png')

        stimuli['fb_correct'] = visual.TextStim(
            self.win,
            text='+',
            color='Green',
            height=0.2,
            pos=[0.0, -0.2])

        stimuli['fb_incorrect'] = visual.TextStim(
            self.win,
            text='x',
            color='Red',
            height=0.2,
            pos=[0.0, -0.2])

        return stimuli

    # Which response buttons to use
    def responseType(self):
        from psychopy import event
        if self.mri_scan:
            # According to Karolinska scanner
            resp = event.getKeys(keyList=['4', '3'])
        else:
            # If running outside the scanner (include keyboard responses)
            resp = event.getKeys(keyList=['4', '3', 'a', 'l', 'space'])
        return resp

    # Define the trial loop
    def runTrials(self, trialObj):
        from psychopy import event
        self.trialhandler = trialObj
        self.countTrials = 0
        print(self.frameR)

        # Timing based on frames and frame rate
        self.targetFrames = int(self.frameR * self.numTime)
        self.itiFrames = int(self.frameR * self.maskTime)

        for trial in self.trialhandler:
            trial['GlobalTimeStamp'] = self.globalClock.getTime()
            self.timer = core.Clock()
            self.timer.reset()
            if trial['Stimulus'] != '0':
                self.stim['number'].setText(trial['Stimulus'])
                for frame in range(self.targetFrames):
                    self.stim['number'].draw()
                    self.win.flip()
                    response = self.responseType()
                    if response:
                        trial['Response'] = '1'
                        trial['RT'] = self.timer.getTime()
                for frame in range(self.itiFrames):
                    self.stim['mask'].draw()
                    self.win.flip()
                    response = self.responseType()
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
            else:
                mwResp = self.mw.rating()
                trial['Type'] = mwResp['Type']
                if mwResp['Type'] == 'MWdual' or mwResp['Type'] == 'MWLikert':
                    trial['dualWhereResp'] = mwResp['Response where']
                    trial['dualAwareResp'] = mwResp['Response aware']
                    trial['dualWhereRT'] = mwResp['RT where']
                    trial['dualAwareRT'] = mwResp['RT aware']
                elif mwResp['Type'] == 'MWmulti':
                    trial['multiResp'] = mwResp['Response']
                    trial['multiRT'] = ['RT']

            trial['trialTimeStamp'] = self.timer.getTime()
            trial['Time'] = time.strftime("%H:%M:%S")
            trial['Trial'] = self.countTrials
            self.log.append(trial)

            if event.getKeys(keyList=["escape"]):
                core.quit()

    # Define the training loop
    def runTraining(self, trialObj):
        from psychopy import event
        self.trialhandler = trialObj
        self.countTrials = 0
        print(self.frameR)

        # Timing based on frames and frame rate
        self.targetFrames = int(self.frameR * self.numTime)
        self.itiFrames = int(self.frameR * self.maskTime)

        for trial in self.trialhandler:
            trial['GlobalTimeStamp'] = self.globalClock.getTime()
            self.timer = core.Clock()
            self.timer.reset()
            if trial['Stimulus'] != '0':
                self.stim['number'].setText(trial['Stimulus'])
                for frame in range(self.targetFrames):
                    self.stim['number'].draw()
                    self.win.flip()
                    response = self.responseType()
                    if response:
                        trial['Response'] = '1'
                        trial['RT'] = self.timer.getTime()
                for frame in range(self.itiFrames):
                    self.stim['mask'].draw()
                    self.win.flip()
                    response = self.responseType()
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

                # feedback during training if incorrect
                if trial['Accuracy'] == '0' and self.countTrials < 26:
                    for frame in range(self.targetFrames):
                        self.stim['fb_incorrect'].draw()
                        self.win.flip()

                self.countTrials += 1  # add 1 to count

                if self.countTrials == 26:
                    self.instr.start('training2')
            else:
                mwResp = self.mw.rating()
                trial['Type'] = mwResp['Type']
                if mwResp['Type'] == 'MWdual' or mwResp['Type'] == 'MWLikert':
                    trial['dualWhereResp'] = mwResp['Response where']
                    trial['dualAwareResp'] = mwResp['Response aware']
                    trial['dualWhereRT'] = mwResp['RT where']
                    trial['dualAwareRT'] = mwResp['RT aware']
                elif mwResp['Type'] == 'MWmulti':
                    trial['multiResp'] = mwResp['Response']
                    trial['multiRT'] = ['RT']

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
        import mindwandering
        self.win = self.expWindow()

        # self.mw = mindwandering.mwDual(self.win)  # dual response
        self.mw = mindwandering.mwLikert(self.win)  # 7-likert response
        self.instr = self.instructions()
        self.stim = self.createStim()
        self.frameR = self.win.getActualFrameRate()
        if not self.frameR:
            self.frameR = 60.0

        # Log file
        self.log = self.logging()

        # Instructions
        self.instr.start('sartintro')
        self.instr.start('probeintro')
        if self.training:
            self.instr.start('training')

        # Create trials
        self.trials = self.createTrials()
        print('trials created -----------------------------------')
        trialsToRun = self.experimentTrials(self.trials)
        print('trials set -----------------------------------')
        self.log.createFile(trialsToRun[0])
        print('log is set -----------------------------------')

        # If MRI, wait for sync pulse
        if self.mri_scan:
            self.MRI()  # wait for MRI pulse
            # print(self.globalClock.getTime())
            print('MRI launched -----------------------------------')
        else:
            self.globalClock.reset()

        # Run trials
        if not self.training:
            self.runTrials(trialsToRun)
        elif self.training:
            self.runTraining(trialsToRun)

        # End instruction
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
