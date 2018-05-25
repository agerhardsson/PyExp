#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division
import time, os
from psychopy import event, visual, core

class kss:
    def __init__(self,
                 win,
                 subject_id,
                 use_mouse=True,
                 textcol='white'):
        self.win = win
        self.subject_id = subject_id
        left=-0.5
        top=0.4
        self.right=-0.5
        bottom=-0.4
        txsize=0.1
        textcol=textcol
        self.use_mouse=use_mouse

    # Create custom mouse for mouse selection ---------------------------------
        self.mouse = visual.CustomMouse(win=self.win,
                                   leftLimit=left,
                                   topLimit=top,
                                   rightLimit=self.right,
                                   bottomLimit=bottom,
                                   pointer=None,
                                   visible=False)

    # Create marker for selection ---------------------------------------------
        self.spot = visual.Circle(win=self.win,
                                  radius=0.04,
                                  lineColor=textcol,
                                  lineWidth=3)
    # create the kss scale ----------------------------------------------------
        self.kss_scale = []

        text = visual.TextStim(
            win=self.win,
            text=u'Hur sömnig har du känt dig under de senaste 5 minuterna?',
            alignHoriz='center',
            pos=[0, 0.7],
            height=0.08,
            wrapWidth=1.8,
            color=textcol)

        self.kss_scale.append(text)

        kss_alt = [
            u'1    Extremt pigg',
            u'2    Mycket pigg',
            u'3    Pigg',
            u'4    Ganska pigg',
            u'5    Varken pigg eller sömnig',
            u'6    Lätt sömnig',
            u'7    Sömnig men ej ansträngande vara vaken',
            u'8    Sömnig och något ansträngande att vara vaken',
            u'9    Mycket sömnig, mycket ansträngande att vara vaken,\n' +
                 u'      kämpar mot sömnen',]
        kss_pos = top+0.1
        self.kss_set_pos = []

        for i in range(0, len(kss_alt)):

            text = visual.TextStim(
                win=self.win,
                text=kss_alt[i],
                alignHoriz='left',
                pos=[self.right, kss_pos],
                height=0.07,
                wrapWidth=1.8,
                color=textcol)

            if i < len(kss_alt)-1:
                kss_pos = kss_pos-0.1
            else:
                kss_pos = kss_pos-0.14  # last item needs two rows

            text.setPos(newPos=[self.right, kss_pos])
            self.kss_scale.append(text)
            self.kss_set_pos.append(kss_pos)

        self.routine_time = core.Clock()
        self.history = []

    # Run the rating scale ----------------------------------------------------
    def draw(self):
        event.clearEvents(eventType='keyboard')
        self.mouse.resetClicks()
        print self.mouse.getClicks()
        continueRoutine = True
        press = False
        kss_answer = '.'
        rt = '.'
        theseKeys = []
        self.routine_time.reset()

        while continueRoutine is True:
            t = self.routine_time.getTime()

            if self.use_mouse is True:
                for a in range(0, len(self.kss_scale)):
                    self.kss_scale[a].draw()
                self.spot.setPos((self.mouse.getPos()[0]+0.01,
                                  round(self.mouse.getPos()[1], 1)))
                self.spot.draw()
                self.mouse.draw()
                self.win.flip()

                if self.mouse.getClicks() > 0:
                    kss_answer = str(abs(round(self.mouse.getPos()[1], 1)*10-5))
                    rt = t
                    core.wait(.2)
                    press = True

            elif self.use_mouse is False:
                theseKeys = event.getKeys(
                    keyList=['1', '2', '3', '4', '5', '6', '7', '8', '9',
                            'num_1', 'num_2', 'num_3','num_4', 'num_5',
                            'num_6', 'num_7', 'num_8', 'num_9'])

                for a in range(0, len(self.kss_scale)):
                    self.kss_scale[a].draw()
                self.win.flip()

                if len(theseKeys) > 0 and press is False:
                    if '1' in theseKeys or 'num_1' in theseKeys:
                        kss_answer = '1'
                        self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[0]])
                    elif '2' in theseKeys or 'num_2' in theseKeys:
                        kss_answer = '2'
                        self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[1]])
                    elif '3' in theseKeys or 'num_3' in theseKeys:
                        kss_answer = '3'
                        self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[2]])
                    elif '4' in theseKeys or 'num_4' in theseKeys:
                        kss_answer = '4'
                        self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[3]])
                    elif '5' in theseKeys or 'num_5' in theseKeys:
                        kss_answer = '5'
                        self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[4]])
                    elif '6' in theseKeys or 'num_6' in theseKeys:
                        kss_answer = '6'
                        self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[5]])
                    elif '7' in theseKeys or 'num_7' in theseKeys:
                        kss_answer = '7'
                        self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[6]])
                    elif '8' in theseKeys or 'num_8' in theseKeys:
                        kss_answer = '8'
                        self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[7]])
                    elif '9' in theseKeys or 'num_9' in theseKeys:
                        kss_answer = '9'
                        self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[8]+0.04])

                    rt = t

                    for a in range(0, len(self.kss_scale)):
                        self.kss_scale[a].draw()
                    self.spot.draw()
                    self.win.flip()

                    press = True

            if press is True:
                # set answers and position of marker according to answer ------------------
                kss_rt = str(rt)
                core.wait(1.5)
                self.win.flip()
                continueRoutine = False

            if event.getKeys(keyList=["escape"]):
                core.quit()


        self.response = {'date': time.strftime("%d/%m/%Y"),
                    'time': time.strftime("%H:%M:%S"),
                    'answer': kss_answer,
                    'rt': kss_rt}

        self.history.append(self.response)

    def getResponse(self):
        return self.response

    def getHistory(self):
        return self.history

    def clear(self):
        self.response = {}
        self.history = []

    def logFile(self, onlyLatest=False):
        directory = 'data/kss/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = directory + str(self.subject_id) + "_kss_.txt"
        if not os.path.exists(file_path):
            f = open(file_path, "w")
            f.write(
                'subject_id\t'
                + 'date\t'
                + 'time\t'
                + 'kss\t'
                + 'rt\n'
            )
            f.close()

        f = open(file_path, "a")
        if onlyLatest==True:
            f.write(
                str(self.subject_id) + '\t'  # id
                + str(self.response['date']) + '\t'  # date
                + str(self.response['time']) + '\t'  # time
                + str(self.response['answer']) + '\t'  # answer
                + str(self.response['rt']) + '\n' # time to response
            )
        elif onlyLatest==False:
            for h in self.history:
                f.write(
                    str(self.subject_id) + '\t'  # id
                    + str(h['date']) + '\t'  # date
                    + str(h['time']) + '\t'  # time
                    + str(h['answer']) + '\t'  # answer
                    + str(h['rt']) + '\n' # time to response
                )
        f.close()


# --------------------- Example -----------------------------------------------
# ppt = raw_input('Participant: ')
#
# win = visual.Window(fullscr=False, color='black')
#
# kss1 = kss(win, ppt, textcol='white', use_mouse=True)
# print kss1
# kss2 = kss(win, ppt, textcol='white', use_mouse=True)
# print kss2
# quit()
