#!/usr/bin/env python2
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
    global version
    global run_version
    global load_set
    global run_training

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
            version = input('version (1-4): ')
            if version < 1 or version > 4:
                print('Not a valid version choose between 1 and 4')
            else:
                break
        while True:
            load_set = input('set (1-2): ')
            if load_set < 1 or load_set > 2:
                print('Not a valid set choose between 1 and 2')
            else:
                break
        while True:
            bi_mode = raw_input('Bi-mode (y/n): ')
            if bi_mode == 'y':
                run_version = True
                break
            elif bi_mode == 'n':
                    run_version = False
                    break
            else:
                print('Not a valid response (y/n)')

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
                'bi mode': True,
                'training': False
            }
            dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
            if dlg.OK is False:
                print('User pressed cancel')
                core.quit()  # user pressed cancel
            if expInfo['participant'] == '':
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
        version = expInfo['version (1-4)']
        load_set = expInfo['version set (1-2)']
        run_version = expInfo['bi mode']
        run_training = expInfo['training']

    save_participant(participant)


# Load instructions -----------------------------------------------------------
def load_instructions():
    text_list = []

    # Instruction 0
    filename = "instructions/intro1.txt"
    with open(filename, "r") as myfile:
        text = unicode(myfile.read(), 'UTF-8')
        text_list.append(text)

    # Instruction 1
    filename = "instructions/intro2.txt"
    with open(filename, "r") as myfile:
        text = unicode(myfile.read(), 'UTF-8')
        text_list.append(text)

    # Instruction 2
    filename = "instructions/intermed.txt"
    with open(filename, "r") as myfile:
        text = unicode(myfile.read(), 'UTF-8')
        text_list.append(text)

    # Instruction 3
    filename = "instructions/end.txt"
    with open(filename, "r") as myfile:
        text = unicode(myfile.read(), 'UTF-8')
        text_list.append(text)

    return text_list
