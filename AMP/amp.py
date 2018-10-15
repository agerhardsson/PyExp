#!/usr/bin/env python
# -*- coding: utf-8 -*-

from myFunctions import instructions
from psychopy import core, visual
import collections

class amp():

    def __init__(self, fullscreen=False):
        self.Fullscreen = fullscreen

    # Create the window
    def expWindow(self, size=(1280, 800), color='black'):
        self.win = visual.Window(size,
                                 fullscr=self.Fullscreen,
                                 screen=0,
                                 monitor='testMonitor',
                                 color=color,
                                 colorSpace='rgb',
                                 winType='pyglet')
        self.win.mouseVisible = False
        return self.win

        def instructions(self):
            instr = instructions.instructions(self.win)
            return instr

        # Continue here --->
        def loadImageList(self):
            data_array = []
            file = open("Payen2005IAPS/Payen2005IAPS.txt", "r")
            for line in file:
                data = line.split("\t")
                data_array.append(data)
            imgList = []
            imgDict = collections.OrderedDict()
            imgDict[imgList[0]]

        def createStim(self):
            stimuli = {}
            stimuli['pic'] = visual.SimpleImageStim(self.win,
                                                     image=)
