#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import string
from psychopy import event, visual


'''
To do:
- create write to file
- create overwrite protection
'''


class ExperimentInfo():

    def __init__(self,
                 expName='Experiment',
                 infoDict={'variables':
                           ['subject_id', 'version', 'session'],
                           'labels':
                           ['Enter Subject id:', 'Enter version number:',
                            'Enter session:'],
                           'maxInput': [4, 2, 2]},
                 checkDataFolder='data/',
                 onlyNumeric=True):

        self.expInfo = {}
        self.expInfo['date'] = time.strftime("%Y-%m-%d")
        self.expInfo['time'] = time.strftime("%H:%M")
        self.expInfo['exName'] = expName
        # self.labels = labels
        self.infoDict = infoDict
        self.checkDataFolder = checkDataFolder
        self.onlyNumeric = onlyNumeric

    def checkParticipant(self, subject_id):
        participants = []
        for file in os.listdir(self.checkDataFolder):
            if file.endswith('.txt'):
                participants.append(file[9:-4])
            # for i, col_names in enumerate(col_names):
            #     iapsDict[col_names] = by_cols[i]

    def genStim(self):

        stim = {}
        stim['name'] = visual.TextStim(win=self.win,
                                       pos=(0.0, 0.5),
                                       text=self.expInfo['exName'],
                                       height=0.07,
                                       font=u'Arial')
        stim['date'] = visual.TextStim(win=self.win,
                                       pos=(0.0, 0.4),
                                       text=self.expInfo['date'],
                                       height=0.06,
                                       font=u'Arial')
        stim['time'] = visual.TextStim(win=self.win,
                                       pos=(0.0, 0.3),
                                       text=self.expInfo['time'],
                                       height=0.06,
                                       font=u'Arial')
        stim['label'] = visual.TextStim(win=self.win,
                                        text='',
                                        font=u'Arial')
        stim['input'] = visual.TextStim(win=self.win,
                                        pos=(0.0, -0.2),
                                        text='_',
                                        font=u'Arial')
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
        self.win = visual.Window(size=(800, 600),
                                 fullscr=False,
                                 screen=0,
                                 monitor='testMonitor')
        self.win.mouseVisible = False
        return self.win

    def run(self):
        self.win = self.expWindow()
        stim = self.genStim()
        keys = self.genKeys()

        # for label in self.labels:
        for var, lab, max in zip(self.infoDict['variables'],
                                 self.infoDict['labels'],
                                 self.infoDict['maxInput']):
            input = []

            while True:
                stim['name'].setAutoDraw(True)
                stim['date'].setAutoDraw(True)
                stim['time'].setAutoDraw(True)

                stim['label'].setText(lab)
                stim['label'].setAutoDraw(True)
                self.win.flip()
                key = event.getKeys(keyList=keys)
                input.append(key)
                text = ''.join([y for x in input for y in x])
                if len(text) <= max:
                    stim['input'].setText(text)

                stim['input'].setAutoDraw(True)
                self.win.flip()

                if event.getKeys(keyList=['backspace']):
                    input = []
                    stim['input'].setAutoDraw(False)
                    self.win.flip()

                if event.getKeys(keyList=['escape', 'return']):
                    break
            if not self.onlyNumeric:
                self.expInfo[var] = text
            else:
                self.expInfo[var] = format(int(text),
                                           '0' + str(max) + 'd')

        return(self.expInfo)


# ============================================================================
# Example

# expInfo = ExperimentInfo()
# info = expInfo.run()
# print(info)
