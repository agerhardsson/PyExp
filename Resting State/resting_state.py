#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, event, core


# =============================================================================
class resting_state():

    def __init__(self,
                 win,
                 textCol='white'):
        self.textCol = textCol
        self.win = win

        self.frameR = self.win.getActualFrameRate()
        if not self.frameR:
            self.frameR = 60.0

    def createCross(self):
        stimuli = {}
        instr = (u'I detta experiment är din uppgift att fokusera på korset i'
                 u' mitten. Försök att inte tänka på något särskilt.'
                 '\n\n'
                 u'(Tryck mellanslag för att starta)')

        stimuli['instructions'] = visual.TextStim(self.win,
                                                  text=instr,
                                                  color=self.textCol,
                                                  height=0.1)

        stimuli['cross'] = visual.TextStim(self.win,
                                           text='+',
                                           color=self.textCol,
                                           height=0.1)
        return(stimuli)

    def run(self, time=8.0):
        time = time*60
        crossFrames = int(time * self.frameR)
        stim = self.createCross()
        while not event.getKeys(keyList=['space', 'escape']):
            stim['instructions'].draw()
            self.win.flip()
        for frames in range(crossFrames):
            stim['cross'].draw()
            self.win.flip()
            if event.getKeys(keyList=['escape']):
                core.quit()


# Example -------------------------------------------------------------------
win = visual.Window(size=(1280, 800), color='black')

RS = resting_state(win)
RS.run()
