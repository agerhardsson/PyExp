#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created 2020-07-09 by Andreas Gerhardsson
Requieres modules: psychopy, random, os, time
"""

# import modules --------------------------------------------------------------
from psychopy import core, visual, event, gui
from random import uniform
import os
import time

# Settings --------------------------------------------------------------------
ExperimentName = 'PVT'
dataFolder = 'data/'
Fullscreen = True
backgroundColor = 'black'
textColor = 'white'

# Instructions ----------------------------------------------------------------
intro = """
Detta är ett reaktionstest.

Varje försök börjar med ett fixeringskort.

Din uppgift är att trycka mellanslag så snabbt som möjligt
så fort fixeringskorset byts mot en klocka som räknar ner.

Trycker du för tidigt visas FALSE på skärmen.

Tryck mellanslag för att börja

"""

end = """ Nu är testet slut"""


# Dialog box  -----------------------------------------------------------------
class dialog():
    def __init__(self,
                 expName='Experiment'):
        self.expName = expName
        self.dataFolder = dataFolder

    def box(self):
        info = dict(
            subject_id='1',
            session=[1, 2],
            maxTime=10)
        infoDlg = gui.DlgFromDict(info,
                                  title=self.expName,
                                  sortKeys=False,
                                  show=True)
        expInfo = dict(
            subject_id=format(int(info['subject_id']), '0' + '3' 'd'),
            session=format(int(info['session']), '0' + '2' 'd'),
            date=time.strftime("%Y-%m-%d"),
            time=time.strftime("%H:%M"),
            expName=ExperimentName,
            maxTime=info['maxTime']
        )
        expInfo['filename'] = (expInfo['date'] + '_' +
                               expInfo['subject_id'] + "_" +
                               expInfo['session'] + ".txt")

        if infoDlg.OK:
            return(expInfo)
        else:
            print("User Cancelled")
            core.quit()

    def checkSubject(self, dict):
        if not os.path.exists(self.dataFolder):
            os.makedirs(self.dataFolder)
        dir = self.dataFolder

        listTest = []
        for file in os.listdir(dir):
            if file.endswith('.txt'):
                listTest.append(file != dict['filename'])
        return(all(listTest))


# Log function  ---------------------------------------------------------------
class mylogging():

    def __init__(self):
        self.dir = dataFolder

    def createFile(self, data):
        dataKeys = data
        path = os.getcwd()
        directory = path + '/' + dataFolder
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.file = (directory + dataKeys['filename'])
        self.f = open(self.file, "w")
        for key in dataKeys.keys():
            self.f.write(str(key) + '\t')
        self.f.write('\n')
        self.f.close()

    def append(self, dataVals):
        self.dataVals = dataVals
        self.f = open(self.file, "a")
        for value in self.dataVals.values():
            self.f.write(str(value) + '\t')
        self.f.write('\n')
        self.f.close()


# PVT -------------------------------------------------------------------------
class PVT():
    def __init__(self):
        self.time_min = expinfo['maxTime'] * 60

    def window(self):
        self.win = visual.Window(fullscr=Fullscreen, color=backgroundColor)
        self.win.mouseVisible = False
        return self.win

    def instruction(self, instr, addText="", maxTime=180):
        mouse = event.Mouse()
        time = core.Clock()
        self.win.setMouseVisible(False)
        event.clearEvents(eventType='keyboard')
        instrObj = visual.TextStim(
            win=self.win,
            text='',
            font=u'Arial',
            height=0.07,
            alignText='center',
            wrapWidth=1.8,
            color=textColor
        )
        instrObj.setText(instr + addText)
        while not (event.getKeys(keyList=['space']) or
                   sum(mouse.getPressed()) > 0):
            instrObj.setAutoDraw(True)
            self.win.flip()
            if time.getTime() > maxTime:
                break
            if event.getKeys(keyList=['escape']):
                core.quit()
        instrObj.setAutoDraw(False)
        core.wait(0.3)
        self.win.flip()
        core.wait(0.5)

    def stimuli(self):
        self.stim = {}
        self.stim['num'] = visual.TextStim(
            self.win, color=textColor,
            text='')
        self.stim['wait'] = visual.TextStim(
            self.win, color=textColor,
            text='+')
        self.stim['false'] = visual.TextStim(
            self.win, color='red',
            text='FALSE')
        return(self.stim)

    def data(self):
        data = {}
        for key in expinfo:
            data[key] = expinfo[key]
        data['timestamp'] = []
        data['trial'] = []
        data['interval'] = []
        data['rt'] = []
        return(data)

    def logging(self):
        log = mylogging()
        return log

    def start_trials(self):
        # Window
        win = self.window()
        self.frameR = win.getActualFrameRate()
        if not self.frameR:
            self.frameR = 60.0

        mouse = event.Mouse()

        # Set up logging
        data = self.data()
        log = self.logging()
        log.createFile(data)

        # Stimuli
        trial = 0
        stim = self.stimuli()

        # Timers
        time = self.time_min
        globalTimer = core.Clock()
        timer = core.Clock()
        max = core.Clock()
        waitTime = core.Clock()

        self.instruction(intro)

        globalTimer.reset()
        while globalTimer.getTime() < time:
            mouse.clickReset()
            trial += 1
            falseAlarm = False
            rt = ''
            interval = uniform(2, 10)
            waitTime.reset()
            waitTime.add(interval)
            while waitTime.getTime() < 0:
                buttons = mouse.getPressed()
                stim['wait'].draw()
                win.flip()
                if (event.getKeys(keyList=['space']) or sum(buttons) > 0):
                    event.clearEvents()
                    stim['false'].draw()
                    win.flip()
                    core.wait(1)
                    falseAlarm = True
                    break
                if event.getKeys(keyList=['escape']):
                    print('User pressed Escape')
                    core.quit()

            max.reset()
            max.add(9.99)
            timer.reset()
            mouse.clickReset()
            while (waitTime.getTime() > 0 and max.getTime() < 0 and
                   falseAlarm is False):
                keys = event.getKeys(keyList=['space'], timeStamped=timer)
                buttons, mouseRT = mouse.getPressed(getTime=True)
                stim['num'].text = '{:01.3f}'.format(timer.getTime())
                stim['num'].draw()
                win.flip()
                if keys:
                    event.clearEvents()
                    rt = keys[0][1]
                    stim['num'].text = '{:01.3f}'.format(rt)
                    stim['num'].draw()
                    win.flip()
                    core.wait(1.5)
                    break
                elif sum(buttons) > 0:
                    mouse.clickReset()
                    event.clearEvents()
                    rt = min([x for x in mouseRT if x > 0.0])
                    stim['num'].text = '{:01.3f}'.format(rt)
                    stim['num'].draw()
                    win.flip()
                    core.wait(1.5)
                    break

                if event.getKeys(keyList=['escape']):
                    print('User pressed Escape')
                    core.quit()
            data['trial'] = trial
            data['timestamp'] = globalTimer.getTime()
            data['interval'] = str(interval)
            data['rt'] = str(rt)
            log.append(data)
            win.flip()
            core.wait(0.5)

            if event.getKeys(keyList=['escape']):
                print('User pressed escape')
                core.quit()

        self.instruction(end)


# Run dialog box if subject file does not exist -------------------------------
subject_exists = False
while not subject_exists:
    dlg = dialog()
    expinfo = dlg.box()
    print(expinfo)
    subject_exists = dlg.checkSubject(expinfo)

# Start experiment

PVT().start_trials()
