#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time

# Functions for logging and keeping track of all information in the lists.


#   The loggin part is designed as following.
#   There are a number of functions below, set_subject_id() for example.
#   By calling them you update the log information when needed.
#   To write a row to the log file you then just call the function log_event().
#   All the information needed is then already stored in this program
#   (sleep_beauty_log.py).
#
#  -Call function log_init() to create the output file before the experiment
#   starts.

#  -Before writing to log, make following function calls:

#  -Call set_subject_id() to set the subject id number.
#   This needs to be done only once in the experiment.

#  -Also call set_version() to set version numberand training number.
#  This needs to be done only once in the experiment,
#  preferably after the information box in the beginning of the experiment.
#
#  -Call set_answer() when the participant has clicked a response.
#  -Call set_correct_answer() when the correct answer is calculated.
#  -Call set_set_reaction_time() when the reaction time is estimated.

#   Call log_event() to write a row to log.
#   The log_event() fuction collects information
#   set by the earlier described function calls together with some of the
#   information in the randomasation lists.

row = 1
current_block = 0
subject_id = '.'
condition = '.'
version = '.'
time_stamp = '.'
block = '0'
picture_id = '.'
picture = '.'
scale = '.'
reaction_time = '.'


# Functions that control stimuli presentation ---------------------------------
def next_block():
    global current_block
    global row
    global block
    current_block += 1
    row = 1
    block = str(current_block + 1)


def return_next_picture():
    global current_block
    global all_blocks
    global row
    this_row = all_blocks[current_block][row][2]
    row += 1
    return this_row


# Functions for controlling outcomes ------------------------------------------

def set_subject_id(in_subject_id):
    global subject_id
    subject_id = in_subject_id


def set_version(in_version):
    global version
    version = in_version

def set_load_set(in_set):
    global load_set
    load_set = in_set

def set_time_stamp(in_time):
    global time_stamp
    time_stamp = str(in_time)

def set_scale(in_scale):
    global scale
    if in_scale == '\n  Nej,\ninte alls':
        scale = '0'
    elif in_scale == '\n Ja,\n lite':
        scale = '1'
    elif in_scale == '\n\n   Ja,\nganska\nmycket':
        scale = '2'
    elif in_scale == '\n   Ja,\nmycket':
        scale = '3'
    elif in_scale == '\n\n    Ja,\nextremt\nmycket':
        scale = '4'

def set_reaction_time(in_time):
    global reaction_time
    reaction_time = str(in_time)

def find(search_key):
    all_columns = all_blocks[current_block][0]
    count = 0
    for elem in all_columns:
        if elem == search_key:
            return count
        else:
            count += 1


def log_event():
    picture_id = all_blocks[current_block][row - 1][find('picture_id')]

    picture = all_blocks[current_block][row - 1][find('picture')]

    condition = all_blocks[current_block][row - 1][find('condition')]

    f = open(log_file_path, "a")
    f.write(
        subject_id + '\t'  # id
        + condition + '\t'  # condition
        + version + '\t'  # version
        + time.strftime("%d/%m/%Y") + '\t'  # date
        + time.strftime("%H:%M:%S") + '\t'  # time
        + time_stamp + '\t'  # time stamp
        + block + '\t'  # block
        + picture_id + '\t'  # picture id
        + picture + '\t'  # picture name
        + scale + '\t'
        + reaction_time + '\n'      # reaction time
    )
    f.close()

# Initiate log file -----------------------------------------------------------
def log_init(version, subject_id, load_set):
    global file_name
    global log_file_path
    global conditions_version1
    global conditions_version2
    global conditions_version3
    global conditions_version4
    global conditions_training

    if load_set == '1':
        # Load version lists set 1
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

        file_name = "lists/sleep_beauty_s1v4.txt"
        with open(file_name) as f:
            randomization_list = f.read().splitlines()
        for i in range(len(randomization_list)):
            this_row = randomization_list[i].split('\t')
            randomization_list[i] = this_row
        conditions_version4 = randomization_list

    if load_set == '2':
        # Load version lists set 2
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

        file_name = "lists/sleep_beauty_s2v4.txt"
        with open(file_name) as f:
            randomization_list = f.read().splitlines()
        for i in range(len(randomization_list)):
            this_row = randomization_list[i].split('\t')
            randomization_list[i] = this_row
        conditions_version4 = randomization_list

    file_name = "lists/sleep_beauty_training.txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i] = this_row
    conditions_training = randomization_list

    # create data file and write first row (header):
    log_file_path = "data/" + subject_id + ".txt"
    f = open(log_file_path, "w")

    # write required parameters to columns in log file:
    f.write(
        'subject_id\t'
        + 'condition\t'
        + 'version\t'
        + 'date\t'
        + 'time\t'
        + 'time_stamp\t'
        + 'block\t'
        + 'picture_id\t'
        + 'picture\t'
        + 'answer\t'
        + 'scale\t'
        + 'reaction_time\t'
        + 'reaction_time_int\n'
    )

    f.close()

# The function set_version() sets the order of main blocks --------------------
def set_start_version(in_version):
    global all_blocks
    global conditions_version1
    global conditions_version2
    global conditions_version3
    global conditions_version4
    global conditions_training

    if in_version == '1':
        all_blocks = [conditions_training, conditions_version1, conditions_version2,
                      conditions_version3, conditions_version4]
    elif in_version == '2':
        all_blocks = [conditions_training, conditions_version2, conditions_version4,
                      conditions_version1, conditions_version3]
    elif in_version == '3':
        all_blocks = [conditions_training, conditions_version3, conditions_version1,
                      conditions_version4, conditions_version2]
    elif in_version == '4':
        all_blocks = [conditions_training, conditions_version4, conditions_version3,
                      conditions_version2, conditions_version1]
