#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
from psychopy import core

# File reading/writing functions experiment -------------------
# Check if data folder exist, else create it

def instructions():
    directory = 'instructions/'

    instruction_texts = {}
    for file in os.listdir(directory):
        instr = file
        name = file[:-4]
        with open(directory + instr, 'r') as myfile:
            text = unicode(myfile.read(), 'UTF-8')
            instruction_texts[name] = text

    return instruction_texts

# Load participant list
def check_participants(participant):
    directory = "data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    ppt_exists = 0
    ppt_list = []
    filename = str(participant) + ".txt"
    for file in os.listdir("data/"):
        if file.endswith(".txt"):
            ppt = file # [11:] remove first 10 characters (date) of text file
            ppt_list.append(ppt)
            for ppt in ppt_list:
                if filename == ppt:
                    ppt_exists = ppt_exists + 1
    return ppt_exists


def run_setup(useGui=False):
    if useGui == False:

        while True:
            participant = input('Participant ID: ')
            if str(participant) == '':
                print('A least one field is empty')
            elif check_participants(participant)  > 0:
                print('Participant already exist!')
            else:
                break
        while True:
            version = input('version (1-4): ')
            if version < 1 or version > 4:
                print('Not a valid version choose between 1 and 3')
            else:
                break
        while True:
            load_set = input('set (1-2): ')
            if load_set < 1 or load_set > 2:
                print('Not a valid set choose between 1 and 2')
            else:
                break
        while True:
            training = raw_input('Training (y/n): ')
            if training == 'y':
                run_training = True
                break
            elif training == 'n':
                run_training = False
                break
            else:
                print('Not a valid response (y/n)')

    elif useGui == True:
        from psychopy import gui
        # show information box:
        while True:
            # Store info about the experiment session
            expName = u'Aesthetics'
            expInfo = {
                'participant': '',
                'version (1-4)': ['1', '2', '3', '4'],
                'version set (1-2)': ['1', '2'],
                'training': False
            }
            dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
            if dlg.OK is False:
                print('User pressed cancel')
                break
            if expInfo['participant'] == '':
                warning = gui.Dlg(title='Warning')
                warning.addText('A least one field is empty')
                warning.show()
            elif check_participants(participant)  > 0:
                warning = gui.Dlg(title='Warning')
                warning.addText('Participant already exist!')
                warning.show()
            else:
                break

        participant = expInfo['participant']
        version = expInfo['version (1-4)']
        load_set = expInfo['version set (1-2)']
        run_training = expInfo['training']

    return participant, version, load_set, run_training

    # --------------------------------------------------------------------
    process_priority = 'high'  # 'high' or 'realtime'

    if process_priority == 'normal':
        pass
    elif process_priority == 'high':
        core.rush(True)
    elif process_priority == 'realtime':
        # Only makes a diff compared to 'high' on Windows.
        core.rush(True, realtime=True)
    else:
        print 'Invalid process priority:',
        process_priority, "Process running at normal."
        process_priority = 'normal'
