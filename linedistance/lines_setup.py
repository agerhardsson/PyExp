#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os

# File reading/writing functions experiment -------------------
participants = []   # Create an empty list

# Load participant list
def check_participants():
    global ppt_exists
    ppt_exists = 0
    ppt_list = []
    filename = str(participant) + ".txt"
    for file in os.listdir("data/"):
        if file.endswith(".txt"):
            ppt = file[11:] # remove first 10 characters (date) of text file
            ppt_list.append(ppt)
            for ppt in ppt_list:
                if filename == ppt:
                    ppt_exists = ppt_exists + 1
    return ppt_exists

def run_setup(useGui=False):
    global participant

    if useGui == False:
        while True:
            participant = raw_input("Participant ID: ")
            if participant == '':
                print 'A least one field is empty'
            elif check_participants() > 0:
                print 'Participant already exist!'
            else:
                print 'Ok!'
                break
    elif useGui == True:
        from psychopy import gui, core
        # show information box:
        while True:
            # Store info about the experiment session
            expName = u'Align'
            expInfo = {
                'participant': ''}
            dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
            participant = expInfo['participant']
            if dlg.OK is False:
                print('User pressed cancel')
                core.quit()  # user pressed cancel
            if expInfo['participant'] == '':
                warning = gui.Dlg(title='Warning')
                warning.addText('A least one field is empty')
                warning.show()
            elif check_participants() > 0:
                warning = gui.Dlg(title='Warning')
                warning.addText('Participant already exist!')
                warning.show()
            else:
                break



# Load instructions -----------------------------------------------------------
def load_instructions():
    text_list = []

    # Instruction 0
    filename = "intro.txt"
    with open(filename, "r") as myfile:
        text = unicode(myfile.read(), 'UTF-8')
        text_list.append(text)

    # Instruction 2
    filename = "intermed.txt"
    with open(filename, "r") as myfile:
        text = unicode(myfile.read(), 'UTF-8')
        text_list.append(text)

    # Instruction 3
    filename = "end.txt"
    with open(filename, "r") as myfile:
        text = unicode(myfile.read(), 'UTF-8')
        text_list.append(text)

    return text_list

# try -------------------------------------------------------------------------
# run_setup(useGui=False)
