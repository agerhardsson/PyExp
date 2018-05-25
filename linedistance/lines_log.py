#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, time


# Functions that control stimuli presentation ---------------------------------


def init(in_subject_id):
    global file_path
    global subject_id

    subject_id = str(in_subject_id)

    directory = "data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = directory + time.strftime("%Y_%m_%d") + "_" + subject_id + ".txt"
    f = open(file_path, "w")

    f.write(
        'subject_id\t'
        + 'date\t'
        + 'time\t'
        + 'block\t'
        + 'direction\t'
        + 'probedistance\t'
        + 'trial\t'
        + 'target\t'
        + 'reversal\t'
        + 'distance\t'
        + 'response\t'
        + 'reaction_time\n'
    )

    f.close()

def log(in_block, in_direction, in_probedistance, in_trial,
        in_target, in_reversal,
        in_distance, in_resp, in_rt):

    block = str(in_block)
    direction = str(in_direction)
    probedistance = str(in_probedistance)
    trial = str(in_trial)
    target = str(in_target)
    reversal = str(in_reversal)
    distance = str(in_distance)
    response = str(in_resp)
    reaction_time = str(in_rt)


    f = open(file_path, "a")
    f.write(
        subject_id + '\t'                   # id
        + time.strftime("%d/%m/%Y") + '\t'  # date
        + time.strftime("%H:%M:%S") + '\t'  # time
        + block + '\t'
        + direction + '\t'
        + probedistance + '\t'
        + trial + '\t'
        + target + '\t'
        + reversal + '\t'
        + distance + '\t'
        + response + '\t'
        + reaction_time + '\n'
    )

    f.close()
