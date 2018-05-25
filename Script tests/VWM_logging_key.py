#Logging functions for Visuospatial working memory task, 
#main experiment
#Written by Mona Lindgren 2014
import os
import time

fileName = ""
current_block=0
row=1
time_stamp = '0'

def next_block():
    global current_block
    global row
    current_block+=1
    row = 1

def initialize_log():
    #write new participant to file:
    global file_name
    global log_file
    global training_version
    global version
    global conditions_wm2_block1
    global conditions_wm2_block2
    global conditions_wm6_block1
    global conditions_wm6_block2
    global conditions_training_block1
    global conditions_training_block2
        
    #load training lists:
    file_name = "lists/wm2_training_r" + str(training_version) + ".txt"
    with open(file_name) as f:
        randomization_list = unicode(f.read(), 'UTF-8').splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i]= this_row
        
    conditions_training_block1 = randomization_list
    
    file_name = "lists/wm6_training_r" + str(training_version) + ".txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i]= this_row
    
    conditions_training_block2 = randomization_list
    
    # load block lists:
    file_name = "lists/wm2_block1_r" + str(version) + ".txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i]= this_row
    
    conditions_wm2_block1 = randomization_list
    
    file_name = "lists/wm2_block2_r" + str(version) + ".txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i]= this_row
    
    conditions_wm2_block2 = randomization_list
    
    file_name = "lists/wm6_block1_r" + str(version) + ".txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i]= this_row
    
    conditions_wm6_block1 = randomization_list
    
    file_name = "lists/wm6_block2_r" + str(version) + ".txt"
    with open(file_name) as f:
        randomization_list = f.read().splitlines()
    for i in range(len(randomization_list)):
        this_row = randomization_list[i].split('\t')
        randomization_list[i]= this_row
    
    conditions_wm6_block2 = randomization_list
    
    #create file and write first row:
    log_file_path = "data/" + subject_id + ".txt"
    log_file = open( log_file_path, "w" )
    
    #write required parameters to columns in log file:
    log_file.write('subject_id\tversion\ttraining_version\tdate\ttime\ttime_stamp\twm_load\tblock\ttrial\t' + 
    'target_number\tprobe\tmatrix\tmatrix_nr\thit\tfoil\tposition_hittarget\t' +
    'answer\tcorrect_answer\treaction_time\n')
    
def set_first_load(in_load):
    global all_blocks
    global conditions_wm2_block1
    global conditions_wm2_block2
    global conditions_wm6_block1
    global conditions_wm6_block2
    global conditions_training_block1
    global conditions_training_block2
    
    if in_load == 2:
        all_blocks = [conditions_training_block1, conditions_training_block2,
        conditions_wm2_block1, conditions_wm6_block1,
        conditions_wm2_block2, conditions_wm6_block2]

    else:
        all_blocks = [conditions_training_block1, conditions_training_block2,
        conditions_wm6_block1, conditions_wm2_block1,
        conditions_wm6_block2, conditions_wm2_block2]

def return_next_matrix():
    global current_block
    global all_blocks
    global row
    matrix_nr = find('matrix')
    matrix_str = all_blocks[current_block][row][matrix_nr]
    this_matrix = [int(matrix_str[1:2]),int(matrix_str[3:4])]
    row+=1
    return this_matrix
    
def set_subject_id(in_subject_id):
    global subject_id
    subject_id = in_subject_id

def set_time_stamp(in_time):
    global time_stamp
    time_stamp = in_time
    
def set_load(in_load):
    global wm_load
    wm_load = in_load
    
def set_block(in_block):
    global block
    block = in_block

def set_version(in_version):
    global version
    version = in_version

def set_training_version(in_version):
    global training_version
    training_version = in_version

def set_answer(theseKeys):
    global answer
    if 'a' in theseKeys:
        answer = '0'
    elif 'l' in theseKeys:
        answer = '1'
    else:
        answer = '-'
    
def set_correct_answer(in_answer):
    global correct_answer
    correct_answer = str(in_answer)
    
def set_reaction_time(in_time):
    global reaction_time
    reaction_time=str(in_time)

def find(search_key):
    #Columns in text files are not allways in the same order. 
    all_columns = all_blocks[current_block][0]
    count = 0
    for elem in all_columns:
        if elem == search_key:
            return count
        else:
            count+=1
            
def check_correct_answer(theseKeys):
    #key['a'] = A
    #key['l'] = L
    #A-key = no
    #L-key = yes
    
    #Find hit column:
    
    hit = find('hit')
    correct_answer = int(all_blocks[current_block][row-1][hit])

    if correct_answer==1 and 'l' in theseKeys:
        return 1
    elif correct_answer==0 and 'a' in theseKeys:
        return 1
    else:
        return 0
    
def write_log():
    global subject_id
    global time_stamp
    global wm_load
    global block
    global answer
    global correct_answer
    global reaction_time
    global version
    global training_version
    global log_file
    
    trial = all_blocks[current_block][row-1][find('trial')]
    target_number = all_blocks[current_block][row-1][find('target_number')]
    probe = all_blocks[current_block][row-1][find('probe')]
    matrix = all_blocks[current_block][row-1][find('matrix')]
    matrix_nr = all_blocks[current_block][row-1][find('matrix_nr')] 
    hit = all_blocks[current_block][row-1][find('hit')]
    foil = all_blocks[current_block][row-1][find('foil')]
    position_hittarget = all_blocks[current_block][row-1][find('position_hittarget')]
    
    #write to log file:
    log_file.write(subject_id + '\t' + version + '\t' + training_version + '\t' + 
    time.strftime("%d/%m/%Y") + '\t'+
    time.strftime("%H:%M:%S") + '\t' + time_stamp + '\t' + wm_load +
    '\t' + block + '\t' + trial + '\t' + target_number + '\t' + probe +
    '\t' + matrix + '\t' + matrix_nr + '\t' + hit + '\t' + foil + '\t' + 
    position_hittarget + '\t' + answer + '\t' + correct_answer + '\t'+
    reaction_time + '\n')
 
def close_log_file():
    global log_file
    log_file.close()