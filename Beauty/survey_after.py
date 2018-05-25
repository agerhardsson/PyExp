#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules --------------------------------------------------------------
from __future__ import division  # handy tool for division

from psychopy import gui, core
import sys
reload(sys)


def run_survey_after(subject_id):
    q1 = u'1. Vad var ditt generella intryck av bilderna?'
    q2 = u'2. Hur var det att identifiera en känsla av skönhet?'
    q3 = u'3. Vad var ditt generella intryck av bilderna?'
    q4 = u'4. '

    a1 = [u'', u'Mycket Lätt', u'Lätt', u'Varken eller', u'Svårt', u'Mycket Svårt']

    while True:
        expName = u'Aesthetics post-questions'

        expInfo = {q1: '', q2: a1, q3: '', q4: ''}

        dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

        if dlg.OK is False:
            print('User pressed cancel')
            core.quit()
        else:
            break



    # create data file and write first row (header):
    file_path = "data/survey/" + subject_id + "_survey_after.txt"
    f = open(file_path, "w")

    f.write('subject_id' + '\t' + subject_id + '\n' + # id
            q1 + '\t' + q1 + '\n' +
            q2 + '\t' + q2 + '\n' +
            q3 + '\t' + q3 + '\n' +
            q4 + '\t' + q4 + '\n'
            )
    f.close()


# run_survey()
# print(str(q1))
# print(str(q2))
# print(str(q3))
# print(str(q4))
