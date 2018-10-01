#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import os

row = 1
current_block = 0
block = '0'

# Save info about subject_id and version to the logging script: ---------------
directory = "data/"
if not os.path.exists(directory):
    os.makedirs(directory)


# Functions that control stimuli presentation ---------------------------------
def next_block():
    global current_block
    global row
    global block
    current_block += 1
    row = 1
    # block = str(current_block + 1)
    block = str(current_block)


def return_next_picture():
    global row
    if load_set == '1':
        path_set = "images/BW/"
    elif load_set == '2':
        path_set = "images/Col/"
    this_row = all_blocks[current_block][row][2]
    row += 1
    return path_set + this_row


def find(search_key):
    all_columns = all_blocks[current_block][0]
    count = 0
    for elem in all_columns:
        if elem == search_key:
            return count
        else:
            count += 1


def log_event(in_answer, in_rt, in_time_stamp, in_trial):
    picture_id = str(all_blocks[current_block][row - 1][find('picture_id')])
    picture = str(all_blocks[current_block][row - 1][find('picture')])
    condition = str(all_blocks[current_block][row - 1][find('condition')])
    answer = str(in_answer)
    rt = str(in_rt)
    time_stamp = str(in_time_stamp)
    trial = str(in_trial)

    f = open(file_path, "a")
    f.write(
        subject_id + '\t'  # id
        + condition + '\t'  # condition
        + version + '\t'  # version
        + time.strftime("%d/%m/%Y") + '\t'  # date
        + time.strftime("%H:%M:%S") + '\t'  # time
        + time_stamp + '\t'  # time stamp
        + trial + '\t'
        + block + '\t'  # block
        + picture_id + '\t'  # picture id
        + picture + '\t'  # picture name
        + answer + '\t'  # answer
        + rt + '\n'  # time to response
    )
    f.close()


# Initiate log file -----------------------------------------------------------
def log_init(in_version, in_load_set, in_subject_id, in_run_training):
    global all_blocks
    global load_set
    global subject_id
    global file_path
    global version
    global run_training
    run_training = in_run_training
    version = str(in_version)
    subject_id = str(in_subject_id)
    load_set = str(in_load_set)
    file_path = directory + str(subject_id) + ".txt"

    # write required parameters to columns in log file:
    f = open(file_path, "w")
    f.write(
        'subject_id\t'
        + 'condition\t'
        + 'version\t'
        + 'date\t'
        + 'time\t'
        + 'time_stamp\t'
        + 'trial\t'
        + 'block\t'
        + 'picture_id\t'
        + 'picture\t'
        + 'answer\t'
        + 'reaction_time\n'
    )
    f.close()

    if load_set == '1':
        # Load version lists set 1 (Gray scale images)
        file_name = "lists/sleep_beauty_s1v1.txt"
        with open(file_name) as f:
            randomization_list = f.read().splitlines()
        for i in range(len(randomization_list)):
            this_row = randomization_list[i].split('\t')
            randomization_list[i] = this_row
        conditions_version1 = randomization_list

        file_name = "lists/sleep_beauty_s1v2.txt"
        with open(file_name) as f:
            randomization_list = f.read().splitlines()
        for i in range(len(randomization_list)):
            this_row = randomization_list[i].split('\t')
            randomization_list[i] = this_row
        conditions_version2 = randomization_list

        file_name = "lists/sleep_beauty_s1v3.txt"
        with open(file_name) as f:
            randomization_list = f.read().splitlines()
        for i in range(len(randomization_list)):
            this_row = randomization_list[i].split('\t')
            randomization_list[i] = this_row
        conditions_version3 = randomization_list

        file_name = "lists/sleep_beauty_s1training.txt"
        with open(file_name) as f:
            randomization_list = f.read().splitlines()
        for i in range(len(randomization_list)):
            this_row = randomization_list[i].split('\t')
            randomization_list[i] = this_row

        conditions_training = randomization_list

    if load_set == '2':
        # Load version lists set 2 (Color images)
        file_name = "lists/sleep_beauty_s2v1.txt"
        with open(file_name) as f:
            randomization_list = f.read().splitlines()
        for i in range(len(randomization_list)):
            this_row = randomization_list[i].split('\t')
            randomization_list[i] = this_row
        conditions_version1 = randomization_list

        file_name = "lists/sleep_beauty_s2v2.txt"
        with open(file_name) as f:
            randomization_list = f.read().splitlines()
        for i in range(len(randomization_list)):
            this_row = randomization_list[i].split('\t')
            randomization_list[i] = this_row
        conditions_version2 = randomization_list

        file_name = "lists/sleep_beauty_s2v3.txt"
        with open(file_name) as f:
            randomization_list = f.read().splitlines()
        for i in range(len(randomization_list)):
            this_row = randomization_list[i].split('\t')
            randomization_list[i] = this_row
        conditions_version3 = randomization_list

        file_name = "lists/sleep_beauty_s2training.txt"
        with open(file_name) as f:
            randomization_list = f.read().splitlines()
        for i in range(len(randomization_list)):
            this_row = randomization_list[i].split('\t')
            randomization_list[i] = this_row

        conditions_training = randomization_list

    if version == '1':
        all_blocks = [conditions_training,
                      conditions_version2,
                      conditions_version1,
                      conditions_version3]
    elif version == '2':
        all_blocks = [conditions_training,
                      conditions_version3,
                      conditions_version1,
                      conditions_version2]
    elif version == '3':
        all_blocks = [conditions_training,
                      conditions_version2,
                      conditions_version3,
                      conditions_version1]
    elif version == '4':
        all_blocks = [conditions_training,
                      conditions_version1,
                      conditions_version2,
                      conditions_version3]
