#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from psychopy import core
import os


class instructions():

    def __init__(self, window, text_size=0.07,
                 wrapWidth=1.8, color='white',
                 dir_path='/instructions/',
                 key='space'):
        self.tSize = text_size
        self.wrapWidth = wrapWidth
        self.color = color
        self.dir = dir_path
        self.win = window
        self.key = key

    def load_instructions(self):
        self.path = os.getcwd()
        directory = self.path + self.dir

        instructionTextsDict = {}
        for file in os.listdir(directory):
            instr = file
            name = file[:-4]
            with open(directory + instr, 'r') as myfile:
                text = unicode(myfile.read(), 'UTF-8')
                instructionTextsDict[name] = text

        return instructionTextsDict

    def start(self, instr):
        from psychopy import visual, event
        self.instr = instr
        self.win.setMouseVisible(False)
        event.clearEvents(eventType='keyboard')

        instruction_object = visual.TextStim(win=self.win,
                                             text='',
                                             font=u'Arial',
                                             height=self.tSize,
                                             wrapWidth=self.wrapWidth,
                                             color='white')

        instruction_texts = self.load_instructions()

        instruction_object.setText(instruction_texts[self.instr])

        while not event.getKeys(keyList=[self.key]):
            instruction_object.draw()
            self.win.flip()
            if event.getKeys(keyList=['escape']):
                core.quit()
        core.wait(0.5)


# Example --------------------------------------------------
# win = visual.Window()
#
# instruction = instructions(win)
# instruction.start('end')
# instruction.start('intermed')
