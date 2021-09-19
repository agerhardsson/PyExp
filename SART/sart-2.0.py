#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import core, gui, event, visual
from psychopy.hardware.emulator import launchScan
import collections
import time
import os
# import sys
import mindwandering
from kss import kss as KSS


# %% -------- Settings --------------#
ExperimentName = 'SART'
dataFolder = 'data/'
mri = False
Fullscreen = False
WindowSize = (1440, 900)
bgCol = 'black'
textCol = 'white'
nTrials = 560
numTime = .250
maskTime = .900


instText = dict()

instText['sartintro'] = """

I det här testet kommer du få se en siffra (1-9).
Den kommer att visas en kort stund i mitten av skärmen.

Siffran följs av en ikryssad cirkel.

Din uppgift är att trycka med pekfingret för alla siffror UTOM siffran 3.

Svara så snabbt och korrekt som möjligt.

(Tryck på med pekfingret (röd) för att starta)

"""

instText['probeintro'] = """


Under testets gång kommer du då och då bli avbruten med frågor om
i vilken grad du var fokuserad på uppgiften och hur medveten du var om det.

Du svarar genom att flytta markören till
höger (pekfinger, röd) eller vänster (långfinger, grön)
och bekräftar ditt svar med ringfingret (gul).
"""

instText['training'] = """

Du kommer nu att få göra en kortare träningsomgång av uppgiften.

Under denna träningsomgång får du feedback i form av
ett rött kryss när du svarar fel.
Dvs. när du trycker på siffran 3,
eller inte trycker på någon av de andra siffrorna.

Svara så snabbt och korrekt som möjligt.

(Tryck på med pekfingret (röd) för att starta)

"""

instText['training2'] = """

Bra. Nu fortsätter träningen, fast denna gång utan feedback.

Svara så snabbt och korrekt som möjligt.

(Tryck på med pekfingret (röd) för att starta)

"""


instText['task'] = """


Nu startar det riktiga testet.

Din uppgift är att trycka med pekfingret för alla siffror UTOM siffran 3.

Svara så snabbt och korrekt som möjligt.

(Tryck på med pekfingret (röd) för att starta)


"""

instText['end'] = """

Nu är det här testet slut, tack!

Tryck på valfri knapp för att avsluta.

"""


# %% Core settings
globalClock = core.Clock()


# %% ----------- Dialog box ---------------#

def dialog():
    continueRoutine = True
    while continueRoutine:
        info = dict(
            subject_id=1,
            version=1,
            session=1,
            training=1)
        infoDlg = gui.DlgFromDict(info,
                                  title=ExperimentName,
                                  sortKeys=False,
                                  show=True)
        expInfo = dict(
            subject_id=format(int(info['subject_id']), '0' + '3' 'd'),
            version=format(int(info['version']), '0' + '2' 'd'),
            session=format(int(info['session']), '0' + '2' 'd'),
            training=info['training'],
            date=time.strftime("%Y%m%d"),
            time=time.strftime("%H%M"),
            expName=ExperimentName
        )
        expInfo['filename'] = (expInfo['date'] + '_' +
                               expInfo['subject_id'] + "_" +
                               expInfo['version'] + "_" +
                               expInfo['session'] + ".txt")
        continueRoutine = expInfo['filename'] in os.listdir(dataFolder)
        if infoDlg.OK:
            print('Subject already exists!')
        else:
            print("User Cancelled")
            core.quit()
    return(expInfo)


# %% ---------------- Logging ------------------------#


def log(dataDict, filename):

    os.makedirs(dataFolder, exist_ok=True)
    file = './' + dataFolder + filename

    if not os.path.exists(file):
        f = open(file, "w")
        for key in dataDict.keys():
            f.write(str(key) + '\t')
        f.write('\n')
        for value in dataDict.values():
            f.write(str(value) + '\t')
        f.write('\n')
        f.close()
    else:
        f = open(file, "a")
        for value in dataDict.values():
            f.write(str(value) + '\t')
        f.write('\n')
        f.close()


# %% ---------------- Window ------------------------#
def expWindow():
    win = visual.Window(size=WindowSize,
                        fullscr=Fullscreen,
                        color=bgCol,
                        colorSpace='rgb',
                        winType='pyglet')
    return(win)


# %% ---------------- Instructions ------------------#

def instruction(win, text):
    instruction = visual.TextStim(win, text='', font='Arial')

    instruction.text = text

    while not event.getKeys(['space']):
        instruction.draw()
        win.flip()
        if event.getKeys(keyList=['escape']):
            win.close()
            core.quit()
    core.wait(0.3)
    win.flip()
    core.wait(0.3)


# %%  ---------------- KSS ------------------------#
def kss(win):
    kss_scale = KSS(win, textCol=textCol)
    kssResp = kss_scale.rating()
    kss_scale.log(subjId=expinfo['subject_id'], dataDict=kssResp)


# %% ---------------- MRI trigger ---------------------#
def MRI(win):
    # Recieves MRI pulse, needed to sync timing with scanner
    MR_settings = {
        'TR': 2.000,  # duration (sec) per volume
        'volumes': 210,  # number of whole-brain 3D volumes / frames
        'sync': 's',     # character to use as the sync timing event;
                      # assumed to come at start of a volume
        'skip': 0,  # number of volumes lacking a sync pulse at start
                    # scan (for T1 stabilization)
        'sound': False,
        }
    launchScan(
        win, MR_settings,
        mode=u'Scan',  # also takes 'Test'
        globalClock=globalClock,
        log=False)


# Create trial lists based on pre-defined lists on text-files
def createTrials():
    # import trial lists
    if expinfo['version'] == '01':
        f = open('lists/list_5.txt', 'r')
    elif expinfo['version'] == '02':
        f = open('lists/list_6.txt', 'r')
    elif expinfo['version'] == u'tr':
        f = open('lists/list_training.txt', 'r')

    expinfo['list'] = f.name[6:]
    trials = f.read().split('\n')
    return(trials[0:nTrials])

# Create the trial list and assign what to be written on data file
def experimentTrials(trials):
    # self.exp = expinfo
    trialList = []  # change to dict?
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

        trialList.append(dataList)

    return(trialList)


# %% -------- Task --------------#
class sart():

    if expinfo['training'] == 1:
        ntrials = 47
        training = True

    

    # def createTrials(self):
        # For future, create a python randomizer

    

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

    # Define experiment
    def startexp(self):
        self.win = self.expWindow()

        # self.mw = mindwandering.mwDual(self.win)  # dual response
        self.mw = mindwandering.mwLikert(self.win)  # 7-likert response

        self.stim = self.createStim()
        self.frameR = self.win.getActualFrameRate()
        if not self.frameR:
            self.frameR = 60.0

        # Log file
        self.log = self.logging()

        self.kss()
        # Instructions
        self.instruction('sartintro')
        self.instruction('probeintro')
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


# %% Run experiment

expinfo = dialog()



run = sart(fullscreen=Fullscreen,
           screen_size=WindowSize,
           screen_color=bgCol,
           nTrials=nTrials,
           numTime=numTime,
           maskTime=maskTime
           )

run.startexp()
