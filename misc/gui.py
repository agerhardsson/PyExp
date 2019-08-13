#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import string
from collections import OrderedDict as dict
from psychopy import event, visual, core


'''
Script by Andreas Gerhardson
Latest update: 2019.08.13
'''


class ExperimentInfo():

    def __init__(self,
                 expName='Experiment',
                 infoDict=dict(
                     subject_id=dict(label='Subject ID:', maxinput=3,
                                     prefix='sub'),
                     version=dict(label='Enter version:', maxinput=2),
                     session=dict(label='Enter session:', maxinput=2)),
                 dataFolder="data/"):

        self.expInfo = dict()
        self.expInfo['expName'] = expName
        self.infoDict = infoDict
        self.type = type
        self.dataFolder = dataFolder
        self.defaultInput = ''

        for v in self.infoDict:
            if 'label' not in self.infoDict[v].keys():
                self.infoDict[v]['label'] = '?'
            if 'maxinput' not in self.infoDict[v].keys():
                self.infoDict[v]['maxinput'] = 2
            if 'prefix' not in self.infoDict[v].keys():
                self.infoDict[v]['prefix'] = ''

    def genStim(self):

        stim = {}
        textColor = 'black'
        stim['name'] = visual.TextStim(
            win=self.win,
            pos=(0.0, 0.5),
            text=self.expInfo['expName'],
            height=0.07,
            color=textColor)
        stim['date'] = visual.TextStim(
            win=self.win,
            pos=(0.0, 0.4),
            text=time.strftime("%Y-%m-%d"),
            height=0.06,
            color=textColor)
        stim['time'] = visual.TextStim(
            win=self.win,
            pos=(0.0, 0.3),
            text=time.strftime("%H:%M"),
            height=0.06,
            color=textColor)
        stim['label'] = visual.TextStim(
            win=self.win,
            text='',
            color=textColor)
        stim['input'] = visual.TextStim(
            win=self.win,
            pos=(0.0, -0.2),
            text='',
            color=textColor)
        stim['duplicate'] = visual.TextStim(
            win=self.win,
            pos=(0.0, 0.0),
            text='Subject file already excists, try a different combination',
            color=textColor)
        stim['square'] = visual.Rect(
            win=self.win,
            width=0.5,
            height=0.15,
            pos=(0.0, -0.21),
            fillColor='grey')

        return(stim)

    def genKeys(self):
        # keys = ','.join(string.ascii_letters + string.digits).split(',')
        keys = ','.join(string.digits).split(',')

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
        if not os.path.exists(self.dataFolder):
            os.makedirs(self.dataFolder)
        dir = self.dataFolder

        listTest = []
        for file in os.listdir(dir):
            if file.endswith('.txt'):
                listTest.append(file != dict['filename'])
        return(all(listTest))

    def run(self):
        self.win = self.expWindow()
        self.stim = self.genStim()
        keys = self.genKeys()
        SubjOK = False

        while not SubjOK:
            for var in self.infoDict:
                label = self.infoDict[var]['label']
                max = self.infoDict[var]['maxinput']
                prefix = self.infoDict[var]['prefix']
                text = ''
                while not event.getKeys(keyList=['return', 'space']) \
                        or len(text) == 0:
                    self.stim['square'].draw()
                    self.stim['name'].draw()
                    self.stim['date'].draw()
                    self.stim['time'].draw()

                    self.stim['label'].setText(label)
                    self.stim['label'].draw()

                    key = event.getKeys(keyList=keys)
                    if key:
                        if len(text) < max:
                            text = text + ''.join(key)

                    self.stim['input'].setText(text)
                    self.stim['input'].draw()
                    self.win.flip()

                    if event.getKeys(keyList=['backspace']):
                        text = text[:-1]
                        self.win.flip()

                    if event.getKeys(keyList=['escape']):
                        print('User pressed cancel')
                        core.quit()

                text = format(int(text), '0' + str(max) + 'd')
                self.expInfo[var] = prefix + text

            self.expInfo['date'] = time.strftime("%Y%m%d")
            self.expInfo['time'] = time.strftime("%H%M")

            filename = []
            for var in self.expInfo:
                self.expInfo[var]
                filename.append(self.expInfo[var])
            self.expInfo['filename'] = '_'.join(filename) + '.txt'

            if self.checkSubject(self.expInfo):
                return(self.expInfo)
            else:
                self.stim['duplicate'].draw()
                self.win.flip()
                event.waitKeys(keyList=['return', 'space', 'escape'])
                del self.expInfo['filename']
                event.clearEvents()
                core.wait(0.2)
                continue


# ============================================================================
# Example

expInfo = ExperimentInfo()
info = expInfo.run()
print(info)
