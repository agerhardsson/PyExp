#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import core

# File reading/writing functions experiment -------------------
participants = []   # Create an empty list

# Check if participant # already exists
def check_number(number):
    global participants
    if number in participants:
        return False
    else:
        return True

# Save participant # to list
def save_participant(number):
    global participants
    participants.append(number)
    # write new participant to file:
    f = open("lists/participant_list.txt", "w")
    for line in participants:
        f.write(str(line) + '\n')
    f.close()

# Load participant list
def load_participants():
    global participants
    file_name = "lists/participant_list.txt"
    with open(file_name) as f:
        participants = f.read().splitlines()
    for i in range(len(participants)):
        elem = int(participants[i])
        participants[i] = elem

def run_setup(useGui=False):
    global participant
    global max_time

    load_participants()

    if useGui == False:

        while True:
            participant = input('Participant ID: ')
            if str(participant) == '':
                print('A least one field is empty')
            elif check_number(participant) is False:
                print('Participant already exist!')
            else:
                break

        while True:
            max_time = input('Max time: ')
            if max_time < 1:
                print('Time too short')
            else:
                break

    elif useGui == True:
        from psychopy import gui
        # show information box:
        while True:
            # Store info about the experiment session
            expName = u'PVT'
            expInfo = {
                'participant': '',
                'time (min)': 10
            }
            dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
            if dlg.OK is False:
                print('User pressed cancel')
                core.quit()  # user pressed cancel
            if (expInfo['participant'] == ''):
                warning = gui.Dlg(title='Warning')
                warning.addText('A least one field is empty')
                warning.show()
            elif check_number(int(expInfo['participant'])) is False:
                warning = gui.Dlg(title='Warning')
                warning.addText('Participant already exist!')
                warning.show()
            else:
                break

        participant = expInfo['participant']
        max_time = expInfo['time (min)']

    save_participant(participant)

def load_instructions():
    text_list = []

    # Instruction 0
    filename = "instructions/intro1.txt"
    with open(filename, "r") as myfile:
        text = unicode(myfile.read(), 'UTF-8')
        text_list.append(text)

    # Instruction 1
    filename = "instructions/end.txt"
    with open(filename, "r") as myfile:
        text = unicode(myfile.read(), 'UTF-8')
        text_list.append(text)

    return text_list
