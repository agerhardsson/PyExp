#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import time
import numpy as np
from psychopy import core
import instructions
import gui
import mylogging

'''
Experiment built by Andreas Gerhardsson (2018), based on procedure described in
Hashimoto (2005), and an alternative described in MacCormack & Lindquist (2018)

Use the following time settings:

Payen (2005):
imageTime=0.075,
crossTime=1.000,
maskTime=None,
blankTime=0.125,
pictoTime=0.100,
responseStyle='payen2005'


Hashimoto (2012):
imageTime=0.075,
crossTime=1.000,
maskTime=2.000,
blankTime=0.425,
pictoTime=0.100,
responseStyle='dual'

MacCormack & Lindquist (2018)
imageTime=0.075,
crossTime=0.125,
maskTime=0.125,
blankTime=0.425,  # not used in this test
pictoTime=0.100,
responseStyle='likert'

'''


class amp():

    def __init__(self,
                 bgCol="black",
                 fullscreen=True,
                 winSize=(1280, 800),
                 imgSize=(1024, 768),
                 nTrials=3,
                 imageTime=0.075,
                 crossTime=1.000,
                 maskTime=2.000,
                 blankTime=0.425,
                 pictoTime=0.100,
                 responseStyle='dual',  # 'likert', 'payen2005' other option
                 pictoType='chinese'  # 'japanese' other option

                 ):

        self.bgCol = bgCol
        if self.bgCol == 'white':
            self.textCol = "black"
        else:
            self.textCol = "white"
        self.pictoType = pictoType
        self.Fullscreen = fullscreen
        self.winSize = winSize
        self.imgSize = imgSize
        self.nTrials = nTrials
        self.blankTime = blankTime
        self.imageTime = imageTime
        self.crossTime = crossTime
        self.maskTime = maskTime
        self.pictoTime = pictoTime
        self.responseStyle = responseStyle
        self.timer = core.Clock()

    # Create the window
    def expWindow(self):
        from psychopy import visual
        self.win = visual.Window(size=self.winSize,
                                 fullscr=self.Fullscreen,
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

    def createStim(self):
        from psychopy import visual
        stimuli = {}
        stimuli['cross'] = visual.TextStim(self.win, text='+',
                                           color=self.textCol)
        stimuli['image'] = visual.ImageStim(self.win,
                                            size=self.imgSize, units='pix')
        noiseTexture = np.random.rand(512, 512) * 2.0 - 1
        stimuli['mask'] = visual.GratingStim(self.win, tex=noiseTexture,
                                             size=self.imgSize, units='pix',
                                             interpolate=True)
        stimuli['pict'] = visual.ImageStim(self.win)
        stimuli['spot'] = visual.TextStim(self.win, text='*', height=0.1,
                                          color=self.textCol)
        stimuli['scale'] = visual.RatingScale(
            self.win,
            marker=stimuli['spot'],
            leftKeys=['a', '4', 'left'],
            rightKeys=['l', '3', 'right'],
            acceptKeys=['space', '2', 'down'],
            lineColor=self.bgCol,
            textColor=self.textCol,
            showValue=False,
            showAccept=False,
            markerColor=self.textCol,
            stretch=3,
            size=0.8,
            scale=None,
            labels=(u'Extremt behagligt', u'Varken behagligt eller obehagligt',
                    u'Extremt obehagligt'),
            # labels=(u'Extremt positivt', u'Varken positivt eller negativt',
            #         u'Extremt negativt'),
            noMouse=True,
            markerStart=4
            )

        stimuli['behagligt'] = visual.TextStim(self.win,
                                               text='Behagligt',
                                               pos=[-.5, -.7],
                                               color=self.textCol)
        stimuli['obehagligt'] = visual.TextStim(self.win,
                                                text='Obehagligt',
                                                pos=[.5, -.7],
                                                color=self.textCol)
        stimuli['positiv'] = visual.TextStim(self.win,
                                             text='Positivt',
                                             pos=[-.5, -.7],
                                             color=self.textCol)
        stimuli['negativ'] = visual.TextStim(self.win,
                                             text='Negativt',
                                             pos=[.5, -.7],
                                             color=self.textCol)
        return stimuli

    def loadImageList(self):

        if expinfo['version'] == '01':
            f = open('lists/list_1.txt', 'r')
        elif expinfo['version'] == '02':
            f = open('lists/list_2.txt', 'r')

        expinfo['list'] = f.name[6:]
        lines = f.read().split('\n')

        IAPS_number = []
        IAPS_jpg = []
        Valence = []
        Desc = []
        PictJ = []
        PictC = []
        for x in lines:
            if len(x) > 0:  # ignore empty row
                IAPS_number.append(x.split('\t')[0])
                IAPS_jpg.append(x.split('\t')[1])
                Valence.append(x.split('\t')[2])
                Desc.append(x.split('\t')[3])
                PictJ.append(x.split('\t')[4])
                PictC.append(x.split('\t')[5])

        imgDict = collections.OrderedDict()
        imgDict[IAPS_number[0]] = IAPS_number[1:len(IAPS_number)]
        imgDict[IAPS_jpg[0]] = IAPS_jpg[1:len(IAPS_jpg)]
        imgDict[Valence[0]] = Valence[1:len(Valence)]
        imgDict[Desc[0]] = Desc[1:len(Desc)]
        if self.pictoType == 'japanese':
            imgDict['Pictogram'] = PictJ[1:len(PictJ)]
        elif self.pictoType == 'chinese':
            imgDict['Pictogram'] = PictC[1:len(PictC)]
        return imgDict

    def experimentTrials(self, trials):

        # trialList = []  # change to dict?
        for data in trials:

            dataDict = collections.OrderedDict()
            dataDict['subject_id'] = expinfo['subject_id'][:4]
            dataDict['Session'] = expinfo['session']
            dataDict['Task'] = expinfo['expName']
            dataDict['Version'] = expinfo['version']
            dataDict['List'] = expinfo['list']
            dataDict['Pict type'] = self.pictoType
            dataDict['Date'] = time.strftime('%Y%m%d')
            dataDict['Time'] = time.strftime('%H:%M:%S')
            dataDict['Trial'] = ''
            dataDict['Response'] = ''
            dataDict['RT'] = ''
            dataDict['IAPS.Number'] = ''
            dataDict['IAPSjpg'] = ''
            dataDict['Valence'] = ''
            dataDict['Pictogram'] = ''

        return dataDict

    def logging(self):
        log = mylogging.log()
        return log

    def runScale(self, tLimit):
        from psychopy import event
        runScale = True
        response = {}
        self.timer.reset()
        self.win.flip()
        while runScale:
            self.stim['scale'].draw()
            self.win.flip()
            if not self.stim['scale'].noResponse:
                response['Response'] = str(self.stim['scale'].getRating())
                response['RT'] = str(self.stim['scale'].getRT())
                runScale = False

            elif self.timer.getTime() > tLimit:
                response['Response'] = ''
                response['RT'] = str(self.timer.getTime())
                runScale = False

            if event.getKeys(keyList=['escape']):
                core.quit()

        self.stim['scale'].reset()
        return response

    def runDual(self, trialObj):
        from psychopy import event
        self.crossFrames = int(self.frameR * self.crossTime)
        self.imageFrames = int(self.frameR * self.imageTime)
        self.blankFrames = int(self.frameR * self.blankTime)
        self.pictoFrames = int(self.frameR * self.pictoTime)
        self.maskFrames = int(self.frameR * self.maskTime)
        trial = 0

        for t in range(0, self.nTrials):
            self.stim['image'].setImage('Payen2005IAPS/' +
                                        trialObj['IAPSjpg'][t])
            self.stim['pict'].setImage('Pictogram/' +
                                       self.pictoType + '/' +
                                       self.textCol + '/' +
                                       trialObj['Pictogram'][t])

            trial += 1
            response = {}
            response['Response'] = '0'
            response['RT'] = ''
            self.timer.reset()
            self.stim['scale'].reset()
            for frame in range(self.crossFrames):
                self.stim['cross'].draw()
                self.win.flip()
            for frame in range(self.imageFrames):
                self.stim['image'].draw()
                self.win.flip()
            for frame in range(self.blankFrames):
                self.win.flip()
            for frame in range(self.pictoFrames):
                self.stim['pict'].draw()
                self.win.flip()
            for frame in range(self.maskFrames):
                self.stim['mask'].draw()
                self.stim['behagligt'].draw()
                self.stim['obehagligt'].draw()
                self.theseKeys = event.getKeys(keyList=['left', 'right'])
                for thisKey in self.theseKeys:
                    if thisKey == 'left':
                        response['Response'] = '1'
                        response['RT'] = str(self.timer.getTime())
                        self.stim['spot'].setPos([-.5, -.8])
                        self.theseKeys = []
                    elif thisKey == 'right':
                        response['Response'] = '-1'
                        response['RT'] = str(self.timer.getTime())
                        self.stim['spot'].setPos([.5, -.8])
                        self.theseKeys = []
                    self.stim['spot'].draw()

                self.win.flip()

            self.data['Trial'] = trial
            self.data['Response'] = response['Response']
            self.data['RT'] = response['RT']
            self.data['IAPS.Number'] = trialObj['IAPS.Number'][t]
            self.data['IAPSjpg'] = trialObj['IAPSjpg'][t]
            self.data['Valence'] = trialObj['Valence'][t]
            self.data['Pictogram'] = trialObj['Pictogram'][t]

            self.log.append(self.data)

            if event.getKeys(keyList=['escape']):
                core.quit()

    def runPayen(self, trialObj):
        from psychopy import event
        self.crossFrames = int(self.frameR * self.crossTime)
        self.imageFrames = int(self.frameR * self.imageTime)
        self.blankFrames = int(self.frameR * self.blankTime)
        self.pictoFrames = int(self.frameR * self.pictoTime)
        self.maskFrames = int(self.frameR * self.maskTime)
        trial = 0

        for t in range(0, self.nTrials):
            self.stim['image'].setImage('Payen2005IAPS/' +
                                        trialObj['IAPSjpg'][t])
            self.stim['pict'].setImage('Pictogram/' +
                                       self.pictoType + '/' +
                                       self.textCol + '/' +
                                       trialObj['Pictogram'][t])

            trial += 1
            response = {}
            response['Response'] = '0'
            response['RT'] = ''
            self.timer.reset()
            self.stim['scale'].reset()
            for frame in range(self.crossFrames):
                self.stim['cross'].draw()
                self.win.flip()
            for frame in range(self.imageFrames):
                self.stim['image'].draw()
                self.win.flip()
            for frame in range(self.blankFrames):
                self.win.flip()
            for frame in range(self.pictoFrames):
                self.stim['pict'].draw()
                self.win.flip()

            # for frame in range(self.maskFrames):
            self.stim['mask'].draw()
            self.stim['behagligt'].draw()
            self.stim['obehagligt'].draw()
            self.win.flip()
            self.theseKeys = event.waitKeys(maxWait=6,
                                            keyList=['left',
                                                     'right',
                                                     'escape'])
            if self.theseKeys:
                for thisKey in self.theseKeys:
                    if thisKey == 'left':
                        response['Response'] = '1'
                        response['RT'] = str(self.timer.getTime())
                        self.stim['spot'].setPos([-.5, -.8])

                    elif thisKey == 'right':
                        response['Response'] = '-1'
                        response['RT'] = str(self.timer.getTime())
                        self.stim['spot'].setPos([.5, -.8])

                self.stim['spot'].draw()
                self.theseKeys = []

            self.win.flip()

            self.data['Trial'] = trial
            self.data['Response'] = response['Response']
            self.data['RT'] = response['RT']
            self.data['IAPS.Number'] = trialObj['IAPS.Number'][t]
            self.data['IAPSjpg'] = trialObj['IAPSjpg'][t]
            self.data['Valence'] = trialObj['Valence'][t]
            self.data['Pictogram'] = trialObj['Pictogram'][t]

            self.log.append(self.data)

            if event.getKeys(keyList=['escape']):
                core.quit()

    def runLikert(self, trialObj):
        from psychopy import event
        self.crossFrames = int(self.frameR * self.crossTime)
        self.imageFrames = int(self.frameR * self.imageTime)
        self.maskFrames = int(self.frameR * self.maskTime)
        self.pictoFrames = int(self.frameR * self.pictoTime)
        trial = 0

        for t in range(0, self.nTrials):
            self.stim['image'].setImage('Payen2005IAPS/' +
                                        trialObj['IAPSjpg'][t])
            self.stim['pict'].setImage('Pictogram/' +
                                       self.pictoType + '/' +
                                       self.textCol + '/' +
                                       trialObj['Pictogram'][t])

            trial += 1
            self.timer.reset()
            for frame in range(self.crossFrames):
                self.stim['cross'].draw()
                self.win.flip()
            for frame in range(self.imageFrames):
                self.stim['image'].draw()
                self.win.flip()
            for frame in range(self.maskFrames):
                self.stim['mask'].draw()
                self.win.flip()
            for frame in range(self.pictoFrames):
                self.stim['pict'].draw()
                self.win.flip()

            response = self.runScale(10)

            self.data['Trial'] = trial
            self.data['Response'] = response['Response']
            self.data['RT'] = response['RT']
            self.data['IAPS.Number'] = trialObj['IAPS.Number'][t]
            self.data['IAPSjpg'] = trialObj['IAPSjpg'][t]
            self.data['Valence'] = trialObj['Valence'][t]
            self.data['Pictogram'] = trialObj['Pictogram'][t]

            self.log.append(self.data)

            if event.getKeys(keyList=['escape']):
                core.quit()

    def startexp(self):
        self.win = self.expWindow()
        instructions = self.instructions()
        self.log = self.logging()
        # self.trials = self.createTrials()
        self.trials = self.loadImageList()
        self.data = self.experimentTrials(self.trials)

        # imageList = self.loadImageList('lists/' + expinfo['list'])
        self.stim = self.createStim()

        # Log file
        self.log.createFile(self.data)

        self.frameR = self.win.getActualFrameRate()
        if not self.frameR:
            self.frameR = 60.0
        if self.responseStyle == 'likert':
            instructions.start(self.pictoType)
            self.runLikert(self.trials)
        elif self.responseStyle == 'dual':
            instructions.start(self.pictoType + "2")
            self.runDual(self.trials)
        elif self.responseStyle == 'payen2005':
            instructions.start(self.pictoType + "2")
            self.runPayen(self.trials)
        instructions.start('end')
        self.win.close()


def kss():
    import kss
    win = amp().expWindow()
    kss = kss.kss(win, textCol='white')
    kssResp = kss.rating()
    kss.log(subjId=expinfo['subject_id'], dataDict=kssResp)


# Run experiment ----------------------------------------------------
gui = gui.GUI(expName='AMP')
expinfo = gui.start()

if expinfo != 'User pressed cancel':
    run = amp(fullscreen=True,
              imageTime=0.075,
              crossTime=1.000,
              maskTime=6.000,
              blankTime=0.125,
              pictoTime=0.100,
              responseStyle='payen2005',
              bgCol="black")

    kss()
    run.startexp()
    kss()

# images = amp().loadImageList('Payen2005IAPS/Payen2005IAPS.txt')
# print(images['IAPSjpg'][0:15])
