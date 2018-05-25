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
    global version

    if useGui == False:
        print 'Participant ID: ' # since raw_input seem to fail
        while True:
            participant = raw_input("Participant ID: ")
            if participant == '':
                print 'A least one field is empty'
            elif check_participants() > 0:
                print 'Participant already exist!'
                print 'Participant ID: '
            else:
                print 'Ok!'
                break

        while True:
            version = input('version (1-4): ')
            if version < 1 or version > 4:
                print('Not a valid version choose between 1 and 4')
            else:
                break

    elif useGui == True:
        from psychopy import gui, core
        # show information box:
        while True:
            # Store info about the experiment session
            expName = u'Aesthetics'
            expInfo = {
                'participant': '',
                'version (1-4)': ['1', '2', '3', '4']
            }
            dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
            participant = expInfo['participant']
            version = expInfo['version (1-4)']
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
