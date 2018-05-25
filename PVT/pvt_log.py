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
time_stamp = '.'
block = '1'
answer = '.'
reaction_time = '.'
mindw_answer = '.'
mindw_rt = '.'
task = '.'
max_time = '.'


# Functions for controlling outcomes ------------------------------------------
def set_subject_id(in_subject_id):
    global subject_id
    subject_id = in_subject_id


def set_time_stamp(in_time):
    global time_stamp
    time_stamp = str(in_time)

def set_max_time(in_max_time):
    global max_time
    max_time = str(in_max_time)

def set_trial(in_trial):
    global trial
    trial = str(in_trial)

def set_task(in_task):
    global task
    task = str(in_task)

def set_answer(in_answer):
    global answer
    answer = str(in_answer)

def set_interval(in_interval):
    global interval
    interval = str(in_interval)

def set_mindw_answer(in_mindw):
    global mindw_answer
    mindw_answer = str(in_mindw)

def set_mindw_rt(in_time):
    global mindw_rt
    mindw_rt = str(in_time)

def set_reaction_time(in_time):
    global reaction_time
    reaction_time = str(in_time)

def log_event():
    global time_stamp
    global answer
    global reaction_time
    global log_file_path
    global mindw_answer
    global block


    f = open(log_file_path, "a")
    f.write(
        subject_id + '\t'  # id
        + time.strftime("%d/%m/%Y") + '\t'  # date
        + time.strftime("%H:%M:%S") + '\t'  # time
        + time_stamp + '\t'  # time stamp
        + max_time + '\t'
        + block + '\t'  # block
        + trial + '\t'
        + task + '\t'
        + interval + '\t'
        + answer + '\t'  # answer
        + reaction_time + '\t'
        + mindw_answer + '\t'
        + mindw_rt + '\n'

    )
    f.close()

def log_init(subject_id):
    global file_name
    global log_file_path

    # create data file and write first row (header):
    log_file_path = "data/" + subject_id + ".txt"
    f = open(log_file_path, "w")

    # write required parameters to columns in log file:
    f.write(
        'subject_id\t'
        + 'date\t'
        + 'time\t'
        + 'time_stamp\t'
        + 'max_time\t'
        + 'block\t'
        + 'trial\t'
        + 'task\t'
        + 'interval\t'
        + 'answer\t'
        + 'reaction_time\t'
        + 'mindw_answer\t'
        + 'mindw_rt\n'

    )

    f.close()

# The function set_version() sets the order of main blocks --------------------
def set_start_version(in_version):
    global all_blocks
    global conditions_version1
    global conditions_version2
    global conditions_version3
    global conditions_version4

    if in_version == '1':
        all_blocks = [conditions_version1, conditions_version2,
                      conditions_version3, conditions_version4]
    elif in_version == '2':
        all_blocks = [conditions_version2, conditions_version4,
                      conditions_version1, conditions_version3]
    elif in_version == '3':
        all_blocks = [conditions_version3, conditions_version1,
                      conditions_version4, conditions_version2]
    elif in_version == '4':
        all_blocks = [conditions_version4, conditions_version3,
                      conditions_version2, conditions_version1]
