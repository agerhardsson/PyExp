#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, time


row = 0
current_block = 0

# Functions that control stimuli presentation ---------------------------------
def next_block():
    global current_block
    global row
    global block
    current_block += 1
    row = 0
    block = str(current_block + 1)


def next_row():
    global row
    row += 1

def next_sad():
    global current_block
    global all_blocks
    this_row = all_blocks[current_block][row][4]  # set column of picture
    return this_row


def next_happy():
    global current_block
    global all_blocks
    global row
    this_row = all_blocks[current_block][row][5] # set column of picture
    return this_row


def find(search_key):
    all_columns = all_blocks[current_block][0]
    count = 0
    for elem in all_columns:
        if elem == search_key:
            return count
        else:
            count += 1




def init(in_subject_id, in_version):
    global file_path
    global subject_id
    global start_version
    global conditions_AFv1
    global conditions_AFv2
    global conditions_AMv1
    global conditions_AMv2
    global conditions_BFv1
    global conditions_BFv2
    global conditions_BMv1
    global conditions_BMv2

    subject_id = str(in_subject_id)
    start_version = str(in_version)

    directory = "data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = directory + time.strftime("%Y_%m_%d") + "_" + subject_id + ".txt"
    f = open(file_path, "w")

    f.write(
        'subject_id\t'
        + 'date\t'
        + 'time\t'
        + 'start_version\t'
        + 'list_version\t'
        + 'picture_id\t'
        + 'picture_has\t'
        + 'picture_sas\t'
        + 'haspos\t'
        + 'saspos\t'
        + 'trial\t'
        + 'female\t'
        + 'target\t'
        + 'response\t'
        + 'reaction_time\n'
    )

    f.close()

    # load image lists

    file_name = "lists/AFv1.txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i] = this_row
    conditions_AFv1 = randomization_list

    file_name = "lists/AFv2.txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i] = this_row
    conditions_AFv2 = randomization_list

    file_name = "lists/AMv1.txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i] = this_row
    conditions_AMv1 = randomization_list

    file_name = "lists/AMv2.txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i] = this_row
    conditions_AMv2 = randomization_list

    file_name = "lists/BFv1.txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i] = this_row
    conditions_BFv1 = randomization_list

    file_name = "lists/BFv2.txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i] = this_row
    conditions_BFv2 = randomization_list

    file_name = "lists/BMv1.txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i] = this_row
    conditions_BMv1 = randomization_list

    file_name = "lists/BMv2.txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i] = this_row
    conditions_BMv2 = randomization_list

def log(in_trial, in_target,
        in_haspos, in_saspos,
        in_resp, in_rt):

    trial = str(in_trial)
    target = str(in_target)
    haspos = str(in_haspos)
    saspos = str(in_saspos)
    response = str(in_resp)
    reaction_time = str(in_rt)

    picture_id = all_blocks[current_block][row][find('picture_id')]

    picture_sas = all_blocks[current_block][row][find('picture_sas')]
    picture_has = all_blocks[current_block][row][find('picture_has')]
    list_version = all_blocks[current_block][row][find('version')]

    female = all_blocks[current_block][row][find('female')]

    f = open(file_path, "a")
    f.write(
        subject_id + '\t'                   # id
        + time.strftime("%d/%m/%Y") + '\t'  # date
        + time.strftime("%H:%M:%S") + '\t'  # time
        + start_version + '\t'
        + list_version + '\t'
        + picture_id + '\t'
        + picture_has + '\t'
        + picture_sas + '\t'
        + haspos + '\t'
        + saspos + '\t'
        + trial + '\t'
        + female + '\t'
        + target + '\t'
        + response + '\t'
        + reaction_time + '\n'
    )

    f.close()

# The function set_version() sets the order of main blocks --------------------
def set_start_version(in_version):
    global all_blocks

    if in_version == '1':
        all_blocks = [conditions_AFv1,
                      conditions_AMv1,
                      conditions_BFv1,
                      conditions_BMv1]
    elif in_version == '2':
        all_blocks = [conditions_AFv2,
                      conditions_AMv2,
                      conditions_BFv2,
                      conditions_BMv2]
    elif in_version == '3':
        all_blocks = [conditions_AMv1,
                      conditions_AFv1,
                      conditions_BMv1,
                      conditions_BFv1]
    elif in_version == '4':
        all_blocks = [conditions_AMv2,
                      conditions_AFv2,
                      conditions_BMv2,
                      conditions_BFv2]
