#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules --------------------------------------------------------------
from __future__ import division  # handy tool for division

from psychopy import visual, core, event
import sys, os
reload(sys)

sys.setdefaultencoding('utf8')

class suvery():

    def __init__(self, win, subject_id, text_size):
        self.win = win
        self.subject_id = subject_id
        self.text_size = text_size

        directory = "data/survey/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.survey_file_path = directory + self.subject_id + "_survey_art.txt"
        f = open(self.survey_file_path, "w")
        f.write('subject_id' + '\t' +  # id
                'art1' + '\t' + 'art2' + '\t' + 'art3' + '\t' + 'art4' + '\t' +
                'art5' + '\t' + 'art6' + '\t' + 'art7' + '\t' + 'art8' + '\n')
        f.close()

        self.survey_list = []
        file_name = "instructions/questions_art.txt"
        with open(file_name) as f:
            self.survey_list = f.read().split("\n")

        self.answer_list1 = []
        file_name = "instructions/answers_art1.txt"
        with open(file_name) as f:
            self.answer_list1 = f.read().split("\n")

        self.answer_list2 = []
        file_name = "instructions/answers_art2.txt"
        with open(file_name) as f:
            self.answer_list2 = f.read().split("\n")

        self.survey_object = []
        for i in range(0,len(self.survey_list)):
            self.survey_text = visual.TextStim(self.win,
                                      text=self.survey_list[i],
                                      pos=[-0.3,0.3],
                                      wrapWidth=1,
                                      alignHoriz='left',
                                      height=self.text_size)
            self.survey_object.append(self.survey_text)

        self.answer_object1 = []
        self.answer_pos_list = []
        self.answer_pos = 0.1
        self.answer_pos_v = -0.3
        for i in range(0, len(self.answer_list1)):
            self.answer_text = visual.TextStim(self.win,
                                      text=self.answer_list1[i],
                                      pos=[self.answer_pos_v,self.answer_pos],
                                      wrapWidth=1.8,
                                      alignHoriz='left',
                                      height=self.text_size)
            self.answer_text.setPos(newPos=[self.answer_pos_v, self.answer_pos-i/10])
            self.answer_pos_list.append(self.answer_pos-i/10)
            self.answer_object1.append(self.answer_text)

        self.answer_object2 = []
        for i in range(0, len(self.answer_list2)):
            self.answer_text = visual.TextStim(self.win,
                                      text=self.answer_list2[i],
                                      pos=[self.answer_pos_v,self.answer_pos],
                                      wrapWidth=1.8,
                                      alignHoriz='left',
                                      height=self.text_size)
            self.answer_text.setPos(newPos=[self.answer_pos_v, self.answer_pos-i/10])
            self.answer_object2.append(self.answer_text)


        self.spot = visual.Circle(win=self.win,
                                  radius=0.04,
                                  lineColor='white',
                                  lineWidth=3)

    def set_art_answer(self, theseKeys):

        if '0' in theseKeys or 'num_0' in theseKeys:
            self.art_exp_answer = '0'
            self.spot.setPos(newPos=[self.answer_pos_v+0.01, self.answer_pos_list[0]])
        elif '1' in theseKeys or 'num_1' in theseKeys:
            self.art_exp_answer = '1'
            self.spot.setPos(newPos=[self.answer_pos_v+0.01, self.answer_pos_list[1]])
        elif '2' in theseKeys or 'num_2' in theseKeys:
            self.art_exp_answer = '2'
            self.spot.setPos(newPos=[self.answer_pos_v+0.01, self.answer_pos_list[2]])
        elif '3' in theseKeys or 'num_3' in theseKeys:
            self.art_exp_answer = '3'
            self.spot.setPos(newPos=[self.answer_pos_v+0.01, self.answer_pos_list[3]])
        elif '4' in theseKeys or 'num_4' in theseKeys:
            self.art_exp_answer = '4'
            self.spot.setPos(newPos=[self.answer_pos_v+0.01, self.answer_pos_list[4]])
        elif '5' in theseKeys or 'num_5' in theseKeys:
            self.art_exp_answer = '5'
            self.spot.setPos(newPos=[self.answer_pos_v+0.01, self.answer_pos_list[5]])
        elif '6' in theseKeys or 'num_6' in theseKeys:
            self.art_exp_answer = '6'
            self.spot.setPos(newPos=[self.answer_pos_v+0.01, self.answer_pos_list[6]])


    def log_survey(self):
        f = open(self.survey_file_path, "a")
        f.write(self.subject_id + "\t" + "\t".join(self.art_exp_list))
        f.close()


    def run_survey_art(self):
        self.art_exp_answer = '.'
        continueRoutine = True
        q = 0
        self.set_art_answer('.')
        theseKeys = []
        self.art_exp_list = []

        while continueRoutine:
            if q >= len(self.survey_object) - 1:
                self.log_survey()
                continueRoutine = False
                break
            while q < len(self.survey_object) - 1:
                if q < 3:
                    theseKeys = event.getKeys(
                        keyList=['0', '1', '2', '3', '4', '5', '6',
                                'num_0', 'num_1', 'num_2', 'num_3',
                                'num_4', 'num_5', 'num_6'])
                    self.survey_object[q].setAutoDraw(True)
                    for d in range(0,len(self.answer_object1)):
                        self.answer_object1[d].setAutoDraw(True)

                elif q == 3 or q == 4:
                    theseKeys = event.getKeys(
                        keyList=['0', '1', '2', '3', '4', '5',
                                'num_0', 'num_1', 'num_2', 'num_3',
                                'num_4', 'num_5'])
                    self.survey_object[q].setAutoDraw(True)
                    for d in range(0,len(self.answer_object2)):
                        self.answer_object2[d].setAutoDraw(True)

                elif q > 4:
                    theseKeys = event.getKeys(
                        keyList=['0', '1', '2', '3', '4', '5', '6',
                                'num_0', 'num_1', 'num_2', 'num_3',
                                'num_4', 'num_5', 'num_6'])
                    self.survey_object[q].setAutoDraw(True)
                    for d in range(0,len(self.answer_object1)):
                        self.answer_object1[d].setAutoDraw(True)

                self.win.flip()

                if event.getKeys(keyList=["escape"]):
                    core.quit()

                if len(theseKeys) > 0:
                    self.set_art_answer(theseKeys)
                    self.spot.setAutoDraw(True)
                    self.win.flip()
                    core.wait(0.5)
                    self.spot.setAutoDraw(False)
                    self.survey_object[q].setAutoDraw(False)
                    for d in range(0,len(self.answer_object1)):
                        self.answer_object1[d].setAutoDraw(False)
                    for d in range(0,len(self.answer_object2)):
                        self.answer_object2[d].setAutoDraw(False)

                    q = q+1
                    break
            if continueRoutine:
                self.art_exp_list.append(self.art_exp_answer)
                self.win.flip()
                core.wait(0.5)
                event.clearEvents(eventType='keyboard')

# Test it ---------------------------------------------------------------------
# 
# win = visual.Window([800,500], fullscr=True, monitor='testMonitor', color='black')
#
# subject_id = 'test'
#
# text_size = 0.07
#
# survey = suvery(win=win, subject_id=subject_id, text_size=text_size)
#
#
#
# survey.run_survey_art()
