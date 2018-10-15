#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from future.utils import python_2_unicode_compatible
from psychopy import core
import os
import sys


class instructions():

    def __init__(self, window, text_size=0.07,
                 wrapWidth=1.8, color='white',
                 folderName='instructions',
                 key=['space'], waitAfter=0.5):
        self.tSize = text_size
        self.wrapWidth = wrapWidth
        self.color = color
        self.dir = folderName
        self.win = window
        self.key = key
        self.waitAfter = waitAfter

    def load_instructions(self):
        self.path = os.getcwd()
        directory = self.path + '/' + self.dir + '/'

        instructionTextsDict = {}
        for file in os.listdir(directory):
            instr = file
            name = file[:-4]
            with open(directory + instr, 'r') as myfile:
                if sys.version_info[0] >= 3:
                    text = str(myfile.read())  # for python3
                else:
                    text = unicode(myfile.read(), 'UTF-8')  # for python2
                instructionTextsDict[name] = text

        return instructionTextsDict

    def start(self, instr):
        from psychopy import visual, event
        self.instr = instr
        self.win.setMouseVisible(False)
        event.clearEvents(eventType='keyboard')

        instruction_object = visual.TextStim(
            win=self.win,
            text='',
            font=u'Arial',
            height=self.tSize,
            wrapWidth=self.wrapWidth,
            color='white')

        instruction_texts = self.load_instructions()

        instruction_object.setText(instruction_texts[self.instr])

        while not event.getKeys(keyList=self.key):
            instruction_object.draw()
            self.win.flip()
            if event.getKeys(keyList=['escape']):
                core.quit()
        core.wait(0.3)
        self.win.flip()
        core.wait(self.waitAfter)


# Example --------------------------------------------------
# from psychopy import visual
# win = visual.Window()
#
# instruction = instructions(win)
# instruction.start('end')
