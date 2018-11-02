#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import time
import os
import collections
from psychopy import visual, event, core


class kss():

    def __init__(self, win, textCol='black', textSize=.08):

        self.win = win
        self.textcol = textCol
        self.txsize = textSize
        self.keyList = ['1', '2', '3', '4', '5', '6', '7', '8', '9',
                        'num_1', 'num_2', 'num_3', 'num_4', 'num_5',
                        'num_6', 'num_7', 'num_8', 'num_9']
        self.arrowList = ['up', 'down', 'space']

        # generate position parameters and save in dictionary
        self.pos = {}
        self.pos['left'] = -.5
        self.pos['top'] = .4
        self.pos['right'] = -.5
        self.pos['bottom'] = -.4
        self.pos['quest'] = [self.pos['right'], self.pos['top']+.3]
        self.pos['kss1'] = [self.pos['right'], self.pos['top']]
        self.pos['kss2'] = [self.pos['right'], self.pos['top']-.1]
        self.pos['kss3'] = [self.pos['right'], self.pos['top']-.2]
        self.pos['kss4'] = [self.pos['right'], self.pos['top']-.3]
        self.pos['kss5'] = [self.pos['right'], self.pos['top']-.4]
        self.pos['kss6'] = [self.pos['right'], self.pos['top']-.5]
        self.pos['kss7'] = [self.pos['right'], self.pos['top']-.6]
        self.pos['kss8'] = [self.pos['right'], self.pos['top']-.7]
        self.pos['kss9'] = [self.pos['right'], self.pos['top']-.84]
        self.pos['key1'] = [self.pos['right']-0.05, self.pos['top']]
        self.pos['key2'] = [self.pos['right']-0.05, self.pos['top']-.1]
        self.pos['key3'] = [self.pos['right']-0.05, self.pos['top']-.2]
        self.pos['key4'] = [self.pos['right']-0.05, self.pos['top']-.3]
        self.pos['key5'] = [self.pos['right']-0.05, self.pos['top']-.4]
        self.pos['key6'] = [self.pos['right']-0.05, self.pos['top']-.5]
        self.pos['key7'] = [self.pos['right']-0.05, self.pos['top']-.6]
        self.pos['key8'] = [self.pos['right']-0.05, self.pos['top']-.7]
        self.pos['key9'] = [self.pos['right']-0.05, self.pos['top']-.8]

    # Create marker for selection
    def createMarker(self):
        marker = {}
        # marker['spot'] = visual.Circle(win=self.win,
        #                                radius=0.04,
        #                                lineColor=self.textcol,
        #                                lineWidth=3)

        marker['spot'] = visual.TextStim(win=self.win,
                                         text='>',
                                         height=self.txsize,
                                         color=self.textcol)

        return marker

    # create the kss scale ----------------------------------------------------
    def scale(self, draw_it):
        kssDict = collections.OrderedDict()
        kssDict['kssText'] = [
            u'Hur sömnig har du känt dig under de senaste 5 minuterna?',
            u'1\tExtremt pigg',
            u'2\tMycket pigg',
            u'3\tPigg',
            u'4\tGanska pigg',
            u'5\tVarken pigg eller sömnig',
            u'6\tLätt sömnig',
            u'7\tSömnig men ej ansträngande vara vaken',
            u'8\tSömnig och något ansträngande att vara vaken',
            u'9\tMycket sömnig, mycket ansträngande att vara vaken,\n' +
            u'\tkämpar mot sömnen']
        kssDict['altPos'] = [self.pos['quest'],
                             self.pos['kss1'],
                             self.pos['kss2'],
                             self.pos['kss3'],
                             self.pos['kss4'],
                             self.pos['kss5'],
                             self.pos['kss6'],
                             self.pos['kss7'],
                             self.pos['kss8'],
                             self.pos['kss9'],
                             ]
        kssStimList = []
        for val in range(0, 10):
            kssStim = visual.TextStim(
                win=self.win,
                text=kssDict['kssText'][val],
                alignHoriz='left',
                pos=kssDict['altPos'][val],
                height=self.txsize,
                wrapWidth=1.8,
                color=self.textcol)
            kssStimList.append(kssStim)

        for val in range(0, 10):
            kssStimList[val].setAutoDraw(draw_it)

    # set response and marker position according to keyboard response ---------
    def key_answer(self):

        if '1' in self.theseKeys or 'num_1' in self.theseKeys:
            keyResp = '1'
            self.marker['spot'].setPos(self.pos['key1'])
        elif '2' in self.theseKeys or 'num_2' in self.theseKeys:
            keyResp = '2'
            self.marker['spot'].setPos(self.pos['key2'])
        elif '3' in self.theseKeys or 'num_3' in self.theseKeys:
            keyResp = '3'
            self.marker['spot'].setPos(self.pos['key3'])
        elif '4' in self.theseKeys or 'num_4' in self.theseKeys:
            keyResp = '4'
            self.marker['spot'].setPos(self.pos['key4'])
        elif '5' in self.theseKeys or 'num_5' in self.theseKeys:
            keyResp = '5'
            self.marker['spot'].setPos(self.pos['key5'])
        elif '6' in self.theseKeys or 'num_6' in self.theseKeys:
            keyResp = '6'
            self.marker['spot'].setPos(self.pos['key6'])
        elif '7' in self.theseKeys or 'num_7' in self.theseKeys:
            keyResp = '7'
            self.marker['spot'].setPos(self.pos['key7'])
        elif '8' in self.theseKeys or 'num_8' in self.theseKeys:
            keyResp = '8'
            self.marker['spot'].setPos(self.pos['key8'])
        elif '9' in self.theseKeys or 'num_9' in self.theseKeys:
            keyResp = '9'
            self.marker['spot'].setPos(self.pos['key9'])
        return keyResp

    # Run the rating scale ----------------------------------------------------
    def rating(self):
        self.timer = core.Clock()
        self.marker = self.createMarker()
        event.clearEvents(eventType='keyboard')
        self.timer.reset()
        kssResp = {}
        self.scale(True)

        while True:
            self.theseKeys = event.getKeys(keyList=self.keyList)
            self.win.flip()
            if self.theseKeys:
                kssResp['kssAnswer'] = self.key_answer()
                kssResp['kssRT'] = self.timer.getTime()
                self.marker['spot'].draw()
                self.win.flip()
                break

        core.wait(1.5)
        self.win.flip()
        return kssResp

        if event.getKeys(keyList=["escape"]):
            core.quit()

    # create log function -----------------------------------------------------
    def log(self, subjId, dataDict, folder='kss'):
        dir = folder
        subject_id = subjId
        data = dataDict

        # check if directory exist otherwise create it
        thisPath = os.getcwd()
        directory = thisPath + '/' + dir + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # create log file
        dataFile = (directory + "kss_" + time.strftime("%Y%m%d") + "_" +
                    subject_id + ".txt")

        # check if file excists otherwise, if not create it
        if not os.path.exists(dataFile):
            f = open(dataFile, "w")

            # write required parameters to columns in log file
            f.write(
                'subject_id\t'
                + 'date\t'
                + 'time\t'
                + 'kss_answer\t'
                + 'reaction_time\n'
            )

            f.close()
        # write data to file, new row if same subject id on same date
        f = open(dataFile, "a")
        f.write(
            subject_id + '\t'                   # id
            + time.strftime("%d/%m/%Y") + '\t'  # date
            + time.strftime("%H:%M:%S") + '\t'  # time
            + str(data['kssAnswer']) + '\t'     # kss answer
            + str(data['kssRT']) + '\n'         # reaction time
        )
        f.close()


# --------------------- Example -----------------------------------------------
# # create window
# win = visual.Window(
#     fullscr=False,
#     monitor='testMonitor',
#     allowGUI=None,
#     checkTiming=True
# )
# # logging requieres subject id
# subject_id = '21'
#
# # initiate kss class
# kss = kss(win, textCol='white')
#
# # run scale and save data to object
# kssResp = kss.rating()
#
# # Print object
# print(kssResp)
#
# # or log object
# kss.log(subjId=subject_id, dataDict=kssResp)
