#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division
import time, os
from psychopy import event, visual, core

class kss_class():

    def __init__(self,
                 win,
                 subject_id,
                 textcol='black',
                 use_mouse=False):

        self.win=win
        self.left=-0.5
        self.top=0.4
        self.right=-0.5
        self.bottom=-0.4
        self.txsize=0.1
        self.textcol=textcol
        self.use_mouse=use_mouse
        self.subject_id = subject_id

    # Create custom mouse for mouse selection ---------------------------------
        self.mouse = visual.CustomMouse(win=self.win,
                                   leftLimit=self.left,
                                   topLimit=self.top,
                                   rightLimit=self.right,
                                   bottomLimit=self.bottom,
                                   pointer=None,
                                   visible=False)

        self.mouse.pointer = visual.TextStim(win=self.win,
                                        text='O',
                                        color='black',
                                        height=self.txsize,
                                        alignHoriz='center',
                                        alignVert='center'
                                        )
    # Create marker for selection ---------------------------------------------
        self.spot = visual.Circle(win=self.win,
                                  radius=0.04,
                                  lineColor=textcol,
                                  lineWidth=3)
    # create the kss scale ----------------------------------------------------
        self.kss_scale = []

        self.text = visual.TextStim(
            win=self.win,
            text=u'Hur sömnig har du känt dig under de senaste 5 minuterna?',
            alignHoriz='center',
            pos=[0, 0.7],
            height=0.08,
            wrapWidth=1.8,
            color=textcol)

        self.kss_scale.append(self.text)

        self.kss_alt = [
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
        self.kss_pos = self.top+0.1
        self.kss_set_pos = []

        for i in range(0, len(self.kss_alt)):

            self.text = visual.TextStim(
                win=self.win,
                text=self.kss_alt[i],
                alignHoriz='left',
                pos=[self.right, self.kss_pos],
                height=0.07,
                wrapWidth=1.8,
                color=textcol)

            if i < len(self.kss_alt)-1:
                self.kss_pos = self.kss_pos-0.1
            else:
                self.kss_pos = self.kss_pos-0.14  # last item needs two rows

            self.text.setPos(newPos=[self.right, self.kss_pos])
            self.kss_scale.append(self.text)
            self.kss_set_pos.append(self.kss_pos)

        self.routine_time = core.Clock()

        # check if directory exist otherwise create it ------------------------
        directory = "data/kss/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # create log file -----------------------------------------------------
        self.kss_file_path = directory + self.subject_id + "_kss.txt"
        self.f = open(self.kss_file_path, "w")

        # write required parameters to columns in log file --------------------
        self.f.write(
            'subject_id\t'
            + 'date\t'
            + 'time\t'
            + 'kss_answer\t'
            + 'reaction_time\n'
        )

        self.f.close()

    # set answers and position of marker according to answer ------------------
    def key_answer(self, theseKeys):

        if '1' in self.theseKeys or 'num_1' in self.theseKeys:
            self.kss_answer = '1'
            self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[0]])
        elif '2' in self.theseKeys or 'num_2' in self.theseKeys:
            self.kss_answer = '2'
            self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[1]])
        elif '3' in self.theseKeys or 'num_3' in self.theseKeys:
            self.kss_answer = '3'
            self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[2]])
        elif '4' in self.theseKeys or 'num_4' in self.theseKeys:
            self.kss_answer = '4'
            self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[3]])
        elif '5' in self.theseKeys or 'num_5' in self.theseKeys:
            self.kss_answer = '5'
            self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[4]])
        elif '6' in self.theseKeys or 'num_6' in self.theseKeys:
            self.kss_answer = '6'
            self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[5]])
        elif '7' in self.theseKeys or 'num_7' in self.theseKeys:
            self.kss_answer = '7'
            self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[6]])
        elif '8' in self.theseKeys or 'num_8' in self.theseKeys:
            self.kss_answer = '8'
            self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[7]])
        elif '9' in self.theseKeys or 'num_9' in self.theseKeys:
            self.kss_answer = '9'
            self.spot.setPos(newPos=[self.right+0.01, self.kss_set_pos[8]+0.04])

    # log the response to new row ---------------------------------------------
    def log_kss(self):
        f = open(self.kss_file_path, "a")
        f.write(
            self.subject_id + '\t'                   # id
            + time.strftime("%d/%m/%Y") + '\t'  # date
            + time.strftime("%H:%M:%S") + '\t'  # time
            + self.kss_answer + '\t'                 # kss answer
            + self.kss_rt + '\n'              # reaction time
        )
        f.close()

    # Run the rating scale ----------------------------------------------------
    def rating(self):
        event.clearEvents(eventType='keyboard')
        self.continueRoutine = True
        self.press = False
        self.routine_time.reset()
        self.kss_answer = '.'
        self.rt = '.'
        self.theseKeys = []

        while self.continueRoutine is True:
            self.t = self.routine_time.getTime()

            if self.use_mouse is True:
                self.mouse1, self.mouse2, self.mouse3 = self.mouse.getPressed()

                for a in range(0, len(self.kss_scale)):
                    self.kss_scale[a].draw()
                self.spot.setPos((self.mouse.getPos()[0]+0.01,
                                  round(self.mouse.getPos()[1], 1)))
                self.spot.draw()
                self.mouse.draw()
                self.win.flip()

                if self.mouse1 and self.press is False:
                    self.kss_answer = str(abs(round(self.mouse.getPos()[1], 1)*10-5))
                    self.rt = self.t
                    self.press = True

            elif self.use_mouse is False:
                self.theseKeys = event.getKeys(
                    keyList=['1', '2', '3', '4', '5', '6', '7', '8', '9',
                            'num_1', 'num_2', 'num_3','num_4', 'num_5',
                            'num_6', 'num_7', 'num_8', 'num_9'])

                for a in range(0, len(self.kss_scale)):
                    self.kss_scale[a].draw()
                self.win.flip()

                if len(self.theseKeys) > 0 and self.press is False:
                    self.key_answer(self.theseKeys)
                    self.rt = self.t

                    for a in range(0, len(self.kss_scale)):
                        self.kss_scale[a].draw()
                    self.spot.draw()
                    self.win.flip()

                    self.press = True

            if self.press is True:
                self.kss_rt = str(self.rt)
                self.log_kss()
                core.wait(1.5)
                self.win.flip()
                self.continueRoutine = False

            if event.getKeys(keyList=["escape"]):
                core.quit()



# --------------------- Example -----------------------------------------------
# win = visual.Window(
#     fullscr=False,
#     monitor='testMonitor',
#     allowGUI=None,
#     checkTiming=True
# )
#
# subject_id = '21'
# kss = kss_class(win,
#                 textcol='white', use_mouse=False, subject_id=subject_id)
#
#
# kss.rating()
# kss.rating()
