#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import string
from psychopy import event, visual, core


'''
To do:

'''


class ExperimentInfo():

    def __init__(self,
                 expName='Experiment',
                 variables=['subject_id', 'version', 'session'],
                 labels=['Enter Subject id:', 'Enter version number:',
                         'Enter session:'],
                 maxInput=[4, 2, 2],
                 onlyNumeric=True,
                 dataFolder="data/"):

        self.expInfo = {}
        self.expInfo['date'] = time.strftime("%Y-%m-%d")
        self.expInfo['time'] = time.strftime("%H:%M")
        self.expInfo['expName'] = expName
        self.checkvars = variables
        self.infoDict = {'variables': variables,
                         'labels': labels,
                         'maxInput': maxInput}
        self.onlyNumeric = onlyNumeric
        self.dataFolder = dataFolder

    def genStim(self):

        stim = {}
        textColor = 'black'
        stim['name'] = visual.TextStim(
            win=self.win,
            pos=(0.0, 0.5),
            text=self.expInfo['expName'],
            height=0.07,
            font=u'Arial',
            color=textColor)
        stim['date'] = visual.TextStim(
            win=self.win,
            pos=(0.0, 0.4),
            text=self.expInfo['date'],
            height=0.06,
            font=u'Arial',
            color=textColor)
        stim['time'] = visual.TextStim(
            win=self.win,
            pos=(0.0, 0.3),
            text=self.expInfo['time'],
            height=0.06,
            font=u'Arial',
            color=textColor)
        stim['label'] = visual.TextStim(
            win=self.win,
            text='',
            font=u'Arial',
            color=textColor)
        stim['input'] = visual.TextStim(
            win=self.win,
            pos=(0.0, -0.2),
            text='',
            font=u'Arial',
            color=textColor)
        stim['duplicate'] = visual.TextStim(
            win=self.win,
            pos=(0.0, 0.0),
            text='Subject file already excists, try a different combination',
            font=u'Arial',
            color=textColor)

        return(stim)

    def genKeys(self):
        keys = []
        if not self.onlyNumeric:
            for i in string.ascii_lowercase:
                keys.append(i)
        for i in string.digits:
            keys.append(i)

        return(keys)

    def expWindow(self):
        self.win = visual.Window(size=(600, 400),
                                 fullscr=False,
                                 screen=0,
                                 monitor='testMonitor',
                                 color='white')
        self.win.mouseVisible = False
        return self.win

    def checkSubject(self, dict):
        checkFile = []
        for var in self.checkvars:
            checkFile.append(dict[var])
        checkFile = '_'.join(checkFile)
        listTest = []
        for file in os.listdir(self.dataFolder):
            if file.endswith('.txt'):
                listTest.append(file[9:-4] != checkFile)
        return(any(listTest))

    def run(self):
        self.win = self.expWindow()
        self.stim = self.genStim()
        keys = self.genKeys()
        SubjOK = False

        while not SubjOK:
            for var, lab, max in zip(self.infoDict['variables'],
                                     self.infoDict['labels'],
                                     self.infoDict['maxInput']):
                input = ['0']
                while not event.getKeys(keyList=['return', 'space']):
                    self.stim['name'].draw()
                    self.stim['date'].draw()
                    self.stim['time'].draw()

                    self.stim['label'].setText(lab)
                    self.stim['label'].draw()

                    key = event.getKeys(keyList=keys)
                    input.append(key)
                    text = ''.join([y for x in input for y in x])
                    if len(text) <= max:
                        self.stim['input'].setText(text)

                    self.stim['input'].draw()
                    self.win.flip()

                    if event.getKeys(keyList=['backspace']):
                        input = ['0']
                        self.win.flip()

                    if event.getKeys(keyList=['escape']):
                        core.quit()

                if not self.onlyNumeric:
                    self.expInfo[var] = text
                else:
                    self.expInfo[var] = format(int(text),
                                               '0' + str(max) + 'd')
            if self.checkSubject(self.expInfo):
                return(self.expInfo)
            else:
                self.stim['duplicate'].draw()
                self.win.flip()
                event.waitKeys(keyList=['return', 'space', 'escape'])
                event.clearEvents()
                core.wait(0.2)
                continue


# ============================================================================
# Example

# expInfo = ExperimentInfo()
# info = expInfo.run()
# print(info)
