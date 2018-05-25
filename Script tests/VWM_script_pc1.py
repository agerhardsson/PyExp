 #!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, event, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import os
from VWM_grid import Grid
from load_text1_pc1 import *
from VWM_logging_key import *
import win32api # comment to work on macOS (put # before "import")
import time

#-----------CHANGE VARIABLES HERE------------------------
#Window width:
WIN_WIDTH = 1920

#window height:
WIN_HEIGHT = 1080

#Fullscreen? (True/False)
FS = True

#Fixation cross duration: 
FCD = 0.500000

#Fixation cross delay:
FC_DELAY = 0.500000

#Stimulus presentation duration on VWM6 task:
SPD6 = 0.900000

#Stimulus presentation duration on VWM2 task:
SPD2 = 0.900000

#Probe presentation duration:
PPD = 2.500000

#Inter stimulus interval:
ISI = 0.500000

#Delay phase:
DELAY = 1.500000

#Instruction duration:
INST_DUR = 5.000000

#Instruction text size (height)
TX_SZ = 0.07

#Symbol duration wrong/right answer:
S_DUR = 1.200000


#Start text (u and "" have to be kept)
START = u"Tryck 'mellanslag' för att fortsätta!"

#--------------------------------------------------------
#Import participants list:
load_participants()
load_participants2()

#information box:
while True:
    # Store info about the experiment session
    expName = u'VWM'
    expInfo = {u'participant': u'', u'version (1-8)': u'1',
    u'training version (1 or 2)': u'1', u'wm first load(2/6)': u'2'}
    dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
    if dlg.OK == False: core.quit()  # user pressed cancel
    if check_number(int(expInfo['participant'])) == False:
        win32api.MessageBox(0, 'Participant already exists', 'Warning')
    elif int(expInfo['version (1-8)'])>8 or int(expInfo['version (1-8)'])<1:
        win32api.MessageBox(0, 'Not a valid version!', 'Warning')
    elif int(expInfo['training version (1 or 2)'])>2 or int(expInfo['training version (1 or 2)'])<1:
        win32api.MessageBox(0, 'Not a valid version!', 'Warning')
    elif int(expInfo['wm first load(2/6)'])!=2 and int(expInfo['wm first load(2/6)'])!=6:
        win32api.MessageBox(0, 'Not a valid version!', 'Warning')
    
    else:
        break
#Save participant:
save_participant(expInfo['participant'])

subj_ID = expInfo['participant']

#set subject id in VWM_logging:
set_subject_id(subj_ID)

#There are 6 different versions, ie order of images in the randomization files:
version = expInfo['version (1-8)']

#Set number of version in log file:
set_version(version)

#There are 2 different training versions:
training_version = expInfo['training version (1 or 2)']

#Set number of training version in log file:
set_training_version(training_version)
initialize_log()

#first_load is the choice of block order.
#There are two different orders: training-training-2-6-2-6 and training-training-6-2-6-2:
first_load = int(expInfo['wm first load(2/6)'])

#set first load in log file:
set_first_load(first_load)

# Setup the Window
win = visual.Window(size=(WIN_WIDTH, WIN_HEIGHT), fullscr=FS, screen=0, allowGUI=False, 
    allowStencil=False,
    monitor='testMonitor', color='black', colorSpace='rgb',
    blendMode='avg', useFBO=True
    )

#------------------Routine definitions--------------------------------------
def initialize_components():
    global myGrid
    global text
    global fixationCross
    global image_wrong
    global image_correct
    global image_instructions_1
    global image_instructions_2
    global image_instructions_3
    global image_instructions_4
    global instruction_slide_p1
    global instruction_slide_p2
    global instruction_slide_p3
    global instruction_slide_p4
    global instructions
    global instruction_text_after_training
    global keys
    global answer
    global probe_started
    global matrix1_started
    global matrix2_started
    global matrix3_started
    global matrix4_started
    global matrix5_started
    global matrix6_started
    global routineTimer
    global routine_time
    
    #Initialize grid:
    myGrid = Grid(win)
    #Initialize "please press space bar"-text object:
    text = visual.TextStim(win=win, ori=0, name='text',
        text=START,    font='Arial',
        pos=[0, 0], height=TX_SZ, wrapWidth=None,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0)
    
    #Initialize fixation cross-image object:
    fixationCross = visual.ImageStim(win=win, name='fixation_cross',
        image='images/fixation_cross.png', mask=None,
        ori=0, pos=[0, 0], size=[0.2, 0.3],
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=False, depth=0.0)
    
    #Initialize wrong-answer-image object:
    image_wrong = visual.ImageStim(win=win, name='image_wrong',
        image=u'images/wrong_cross.png', mask=None,
        ori=0, pos=[0, 0], size=[0.2, 0.25*1.6],
        color=[1,1,1], colorSpace=u'rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=False, depth=0.0)
        
    #Initialize correct-answer-image object:
    image_correct = visual.ImageStim(win=win, name='image_correct',
        image=u'images/image_correct.jpg', mask=None,
        ori=0, pos=[0, 0], size=[0.2, 0.2*1.6],
        color=[1,1,1], colorSpace=u'rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=False, depth=0.0)
    
    #Initialize first image in instruction slide:
    image_instructions_1 = visual.ImageStim(win=win, name='image_instruction1',
        image=u'images/image_instruction1.jpg', mask=None,
        ori=0, pos=[0, 0], size=[0.5, 0.5*1.6],
        color=[1,1,1], colorSpace=u'rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=False, depth=0.0)
        
    #Initialize second image in instruction slide:
    image_instructions_2 = visual.ImageStim(win=win, name='image_instruction2',
        image=u'images/image_instruction2.jpg', mask=None,
        ori=0, pos=[0, 0], size=[0.5, 0.5*1.6],
        color=[1,1,1], colorSpace=u'rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=False, depth=0.0)
        
    #Initialize third image in instruction slide:
    image_instructions_3 = visual.ImageStim(win=win, name='image_instruction3',
        image=u'images/image_instruction3.jpg', mask=None,
        ori=0, pos=[0, 0], size=[0.5, 0.5*1.6],
        color=[1,1,1], colorSpace=u'rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=False, depth=0.0)
        
    #Initialize fourth image in instruction slide:
    image_instructions_4 = visual.ImageStim(win=win, name='image_instruction4',
        image=u'images/keyboard_L_VWM.jpg', mask=None,
        ori=0, pos=[0.55, 0], size=[0.4, 0.5*1.6],
        color=[1,1,1], colorSpace=u'rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=False, depth=0.0)

    
    #load instruction slide texts to list: 
    instruction_slide = load_instruction_slide()
    
    #Initialize instruction slide text objects:------>
    thisText = instruction_slide[0]
    instruction_slide_p1 = visual.TextStim(win=win, ori=0, name='ins_slide_p1',
        text=thisText,    font='Arial', alignHoriz='center',
        pos=[0, 0], height=TX_SZ, wrapWidth=1.8,
        color='white', colorSpace='rgb', opacity=1)
        
    thisText = instruction_slide[1]
    instruction_slide_p2 = visual.TextStim(win=win, ori=0, name='ins_slide_p2',
        text=thisText,    font='Arial',
        pos=[0, 0.5], height=TX_SZ, wrapWidth=1.8,
        color='white', colorSpace='rgb', opacity=1)

    thisText = instruction_slide[2]
    instruction_slide_p3 = visual.TextStim(win=win, ori=0, name='ins_slide_p3',
        text=thisText,    font='Arial',
        pos=[0, -0.55], height=TX_SZ, wrapWidth=1.8,
        color='white', colorSpace='rgb', opacity=1)

    thisText = instruction_slide[3]
    instruction_slide_p4 = visual.TextStim(win=win, ori=0, name='ins_slide_p4',
        text=thisText,    font='Arial',
        pos=[0, -0.75], height=TX_SZ, wrapWidth=1.8,
        color='white', colorSpace='rgb', opacity=1)

    #Load block instructions texts to list:
    block_instructions = load_instructions()

    #Initialize block instruction objects:
    instructions = []
    for i in range(3):
        thisText = block_instructions[i]
        instr_x = visual.TextStim(win=win, ori=0, name='ins_slide_x',
        text=thisText,    font='Arial',
        pos=[0, 0], height=TX_SZ, wrapWidth=1.8,
        color='white', colorSpace='rgb', opacity=1)
        instructions.append(instr_x)

    #initialize after-training-instruction object:
    with open("instruction_texts_key/VWM_after_training.txt") as f:
        tmp_text = unicode(f.read(), 'UTF-8')
        
    instruction_text_after_training = visual.TextStim(win=win, ori=0, name='after_training',
        text=tmp_text,    font='Arial',
        pos=[0, 0], height=TX_SZ, wrapWidth=1.8,
        color='white', colorSpace='rgb', opacity=1)
    
    
    #Initialize keyboard:
    key_response = event.BuilderKeyResponse()
    answer = False
    keys = False
    theseKeys = event.getKeys(keyList=['a', 'l'])
    event.clearEvents(eventType='keyboard')
    
    #Initialize help variables:
    answer = False
    keys = False
    matrix1_started = False
    matrix2_started = False
    matrix3_started = False
    matrix4_started = False
    matrix5_started = False
    matrix6_started = False
    probe_started = False

    # Create timers:
    routineTimer = core.CountdownTimer()  # to track time remaining of each routine 
    routine_time = core.Clock()  #local routine time
    
def press_key():  #"Press "'spacebar'" function. Text is changed on row 51
    
    t = 0
    routine_time.reset()  # clock
    text_started=False
    continueRoutine = True
    event.clearEvents(eventType='keyboard')
    while continueRoutine:
        # get current time
        theseKeys = event.getKeys(keyList=['space'])
        t = routine_time.getTime()

        # Show text:
        if t >= 0.0 and text_started == False:
            text_started = True
            text.setAutoDraw(True) # True = object is visable 
        
        # wait for key response:
        if t >= 0.0 and len(theseKeys)>0:
            continueRoutine=False
            event.clearEvents(eventType='keyboard')
            text.setAutoDraw(False) # False = object is hidden in this case on when pressing spacebar
            win.flip()
            break
            
        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()
        
        if continueRoutine:
            win.flip()

def first_instruction():
    #This function renders the first instruction slide in this experiment.
    #Some parts are timed and some are controlled by the 'space'-key.
    
    slide_counter = 1
    
    event.clearEvents(eventType='keyboard')
    theseKeys = []
    continueRoutine = True
    
    #Render first part of instruction slide:
    instruction_slide_p1.setAutoDraw(True)
    win.setMouseVisible(False)
    win.flip()
    
    #Wait for participant to press space, 
    #then render first part of animated example:
    while True:
        theseKeys = event.getKeys(keyList = ['space'])
        if len(theseKeys)>0:
            theseKeys = []
            instruction_slide_p1.setAutoDraw(False)
            event.clearEvents(eventType='keyboard')
            image_instructions_1.setAutoDraw(True)
            win.flip()
            break
            
    routine_time.reset()
    
    #Timed instruction slide:   #Change the timings for longer duration
                                #Whole routine on a timeline so change one will
                                #affect the length of the one after
    while continueRoutine:
        theseKeys = event.getKeys(keyList = ['space'])
        t = routine_time.getTime()
        
        if t>= 1.2 and slide_counter == 1:
            slide_counter+=1
            image_instructions_1.setAutoDraw(False)
            image_instructions_2.setAutoDraw(True)
            
        if t>=2.4 and slide_counter == 2:
            slide_counter+=1
            image_instructions_2.setAutoDraw(False)
            image_instructions_3.setAutoDraw(True)
            instruction_slide_p2.setAutoDraw(True)
   
        if t>= 4.9 and slide_counter == 3:
            slide_counter+=1
            instruction_slide_p3.setAutoDraw(True)
            image_instructions_4.setAutoDraw(True)
            
        if t>=7.9 and slide_counter == 4:
            slide_counter+=1
            instruction_slide_p4.setAutoDraw(True) #last instruction is shown

            event.clearEvents(eventType='keyboard')

        if len(theseKeys)>0 and slide_counter == 5:
            slide_counter+=1
            image_instructions_1.setAutoDraw(False)
            image_instructions_2.setAutoDraw(False)
            image_instructions_3.setAutoDraw(False)
            image_instructions_4.setAutoDraw(False)
            instruction_slide_p1.setAutoDraw(False)
            instruction_slide_p2.setAutoDraw(False)
            instruction_slide_p3.setAutoDraw(False)
            instruction_slide_p4.setAutoDraw(False)
            win.flip()
            continueRoutine = False
            break
            
        if continueRoutine:
            win.flip()
            
        if event.getKeys(keyList=["escape"]):
            core.quit()
    
def fixation_cross():
    #A function that displays a fixation cross. 
    global fixationCross
    
    #Initialize time:
    t = 0
    
    #Reset routine time:
    routine_time.reset()
    
    #Add routine duration to a timer:
    routineTimer.reset()
    routineTimer.add(FCD + FC_DELAY)
    
    #Reset conditions:
    cross_started = False
    hide_cross = False
    
    #Clear all key presses:
    event.clearEvents(eventType='keyboard')
    
    while routineTimer.getTime() > 0:
        # get current time
        t = routine_time.getTime()
        # fixationCross image renders:
        if t >= 0.0 and cross_started == False:
            cross_started == True
            fixationCross.setAutoDraw(True)
            win.flip()
        
        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()
    fixationCross.setAutoDraw(False)
    win.flip()
def WM6():
    global keys
    global counter
    global matrix1_started
    global matrix2_started
    global matrix3_started
    global matrix4_started
    global matrix5_started
    global matrix6_started
    global thisBlock
    global version
    global correct_answer
    
    ST = core.StaticPeriod(screenHz=60)
    ST.start(0.03)
    continueRoutine = True
    show_probe = True
    keys=False
    correct_answer = 0
    probe_started = False
    reaction_time = '-'
    #Reset help variables matrixX_started:
    reset_status()
    myGrid.paint_grid()
    #reset logging variables: 
    set_reaction_time('-')
    set_answer('-')
    set_correct_answer('-')
    event.clearEvents(eventType='keyboard')
    ST.complete()
    
    t = 0
    routine_time.reset()
    routineTimer.reset()
    routineTimer.add(6*SPD6 + 5*ISI + DELAY + PPD)
    win.flip()
    
    while continueRoutine and routineTimer.getTime() > 0:
    
    # get current time
        t = routine_time.getTime()
         
        # *matrix1_WM6_training* updates
        if t >= 0.0 and matrix1_started == False:
            myGrid.paint_dot(return_next_matrix())
            #Set logging info in VWM_logging:
            set_time_stamp(str(time.clock()))
            #Write to log file:
            write_log()
            matrix1_started = True
            
        elif t >= (SPD6) and t < (SPD6+ISI):
            myGrid.hide_dot()
           
        # *matrix2_WM6_training* updates
        if t >= (SPD6+ISI) and matrix2_started == False:
            myGrid.paint_dot(return_next_matrix())
            #Set logging info in VWM_logging:
            set_time_stamp(str(time.clock()))
            #Write to log file:
            write_log()
            matrix2_started = True
            
        elif t >= (2*SPD6 + ISI) and t < 2*(SPD6+ISI):
            myGrid.hide_dot()
            
        # *matrix3_WM6_training* updates
        if t >= 2*(SPD6+ISI) and matrix3_started == False:
            myGrid.paint_dot(return_next_matrix())
            #Set logging info in VWM_logging:
            set_time_stamp(str(time.clock()))
            #Write to log file:
            write_log()
            matrix3_started = True
            
        elif t >= (3*SPD6+ 2*ISI) and t < 3*(SPD6+ISI):
            myGrid.hide_dot()
            
        # *matrix4_WM6_training* updates
        if t >= 3*(SPD6+ISI) and matrix4_started == False:
            myGrid.paint_dot(return_next_matrix())
            #Set logging info in VWM_logging:
            set_time_stamp(str(time.clock()))
            #Write to log file:
            write_log()
            matrix4_started = True
            
        elif t >= (4*SPD6 + 3*ISI) and t < 4*(SPD6+ISI):
            myGrid.hide_dot()
            
        # *matrix5_WM6_training* updates
        if t >= 4*(SPD6+ISI) and matrix5_started == False:
            myGrid.paint_dot(return_next_matrix())
            #Set logging info in VWM_logging:
            set_time_stamp(str(time.clock()))
            #Write to log file:
            write_log()
            matrix5_started = True
            
        elif t >= (5*SPD6 + 4*ISI) and t < 5*(SPD6+ISI):
            myGrid.hide_dot()
            
        # *matrix6_WM6_training* updates
        if t >= 5*(SPD6+ISI) and matrix6_started == False:
            myGrid.paint_dot(return_next_matrix())
            #Set logging info in VWM_logging:
            set_time_stamp(str(time.clock()))
            #Write to log file:
            write_log()
            matrix6_started = True
            
        elif t >= (6*SPD6 + 5*ISI) and t < (6*SPD6 + 5*ISI + DELAY):
            myGrid.hide_dot()
   
        if t >= (6*SPD6 + 5*ISI + DELAY) and probe_started == False:
            probe_started = True
            #Save current time to calculate reaction time:
            timestamp_probe = time.clock()
            myGrid.paint_probe(return_next_matrix())
            event.clearEvents(eventType='keyboard')
        # probe and response phase starts:
        if t >= (6*SPD6 + 5*ISI + DELAY) and t < (6*SPD6 + 5*ISI + DELAY + PPD -win.monitorFramePeriod*0.75):
            theseKeys = event.getKeys(keyList=['a', 'l'])
            if len(theseKeys)>0:
                reaction_time = time.clock() - timestamp_probe
                #set reaction time in VWM_logging:
                set_reaction_time(reaction_time)
                #check correct answer by calling function in VWM_loggging:
                correct_answer = check_correct_answer(theseKeys)
                #set answer in VWM_logging:
                set_answer(theseKeys)
                #set correct answer in VWM_logging 1/0:
                set_correct_answer(correct_answer)
                #Set logging info in VWM_logging:
                set_time_stamp(str(time.clock()))
                keys = True
                myGrid.hide_probe()
                
        elif t >= (6*SPD6 + 5*ISI + DELAY + PPD -win.monitorFramePeriod*0.75):
            myGrid.hide_probe()
            
        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()
            
    myGrid.hide_grid()
    myGrid.hide_probe()
    win.flip()
    #Write log for probe phase:
    write_log()
    
    
def WM2():
    global keys
    global matrix1_started
    global matrix2_started
    global probe_started
    global correct_answer
    
    t = 0
    routine_time.reset()
    routineTimer.reset()
    routineTimer.add(2*SPD2 + ISI + DELAY + PPD)
    
    ST = core.StaticPeriod(screenHz=60)
    ST.start(0.03)
    continueRoutine = True
    show_probe = True
    keys=False
    correct_answer = 0
    probe_started = False
    reaction_time = '-'
    #Reset help variables matrixX_started:
    reset_status()
    myGrid.paint_grid()
    #reset logging variables: 
    set_reaction_time('-')
    set_answer('-')
    set_correct_answer('-')
    event.clearEvents(eventType='keyboard')
    ST.complete()
    
    

    win.flip()
    
    while continueRoutine and routineTimer.getTime() > 0:
        
        # get current time
        t = routine_time.getTime()
        
        # grid 1 is shown:
        if t >= 0.0 and matrix1_started == False:
            dot = return_next_matrix()
            myGrid.paint_dot(dot)
            #Set logging info in VWM_logging:
            set_time_stamp(str(time.clock()))
            #Call log function in VWM_logging:
            write_log()
            matrix1_started = True
          
        elif t >= (SPD2) and t < (SPD2+ISI):
            myGrid.hide_dot()
            win.flip()
            
        # grid 2 is shown:
        if t >= (SPD2+ISI) and matrix2_started == False:
            myGrid.paint_dot(return_next_matrix())
            #Set logging info in VWM_logging:
            set_time_stamp(str(time.clock()))
            #Write to log file:
            write_log()
            matrix2_started = True
        
        elif t >= (2*SPD2 + ISI) and t< (2*SPD2 + ISI + DELAY):
            myGrid.hide_dot()
            
        if t >= (2*SPD2 + ISI + DELAY) and probe_started==False:
            probe_started=True
            #Store time stamp to calculate reaction time:
            timestamp_probe = time.clock()
            myGrid.paint_probe(return_next_matrix())
            event.clearEvents(eventType='keyboard')
        # Probe and response phase starts: 
        if t >= (2*SPD2 + ISI + DELAY) and t < (2*SPD2 + ISI + DELAY + PPD -win.monitorFramePeriod*0.75):

            theseKeys = event.getKeys(keyList=['a', 'l'])
            if len(theseKeys)>0:
                reaction_time = time.clock() - timestamp_probe
                #set reaction time in VWM_logging:
                set_reaction_time(reaction_time)
                #check if correct answer, function in VWM_logging:
                correct_answer = check_correct_answer(theseKeys)
                #set answer in VWM_logging:
                set_answer(theseKeys)
                #set correct answer in VWM_logging 1/0:
                set_correct_answer(correct_answer)
                #Set logging info in VWM_logging:
                set_time_stamp(str(time.clock()))
                
                keys = True
                myGrid.hide_probe()
        elif t >=(2*SPD2 + ISI + DELAY + PPD -win.monitorFramePeriod*0.75):
            myGrid.hide_probe()

        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()
            
    myGrid.hide_probe()
    myGrid.hide_grid()
    win.flip()
    #Write log for probe phase:
    write_log()
    
    
def show_instruction(WM):
    #This function renders the instruction text associated with the two loads (2 and 6). 
    global instructions
    routine_time.reset()
    slide_counter = 0
    event.clearEvents(eventType='keyboard')
    
    continueRoutine = True
    
    #Load next instruction:
    if(WM ==2):
        thisInstruction = instructions[0]
    elif(WM == 6):
        thisInstruction = instructions[1]
    elif(WM == 'end'):
        thisInstruction = instructions[2]
    thisInstruction.setAutoDraw(True)
    
    while continueRoutine:
        t = routine_time.getTime()
        theseKeys = event.getKeys(keyList=['space'])
        if len(theseKeys)>0 and slide_counter == 0:
            slide_counter+=1
            thisInstruction.setAutoDraw(False)
            win.flip()
            continueRoutine = False
            break

        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()
    
        # refresh the screen
        if continueRoutine:
            win.flip()
def instruction_after_training():
    global instruction_text_after_training
    t = 0
    routine_time.reset()
    routineTimer.add(INST_DUR)
    event.clearEvents(eventType='keyboard')
    #Show instruction:
    instruction_text_after_training.setAutoDraw(True)  
    
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = routine_time.getTime()
        theseKeys = event.getKeys(keyList=['space'])
        if len(theseKeys)>0:
            instruction_text_after_training.setAutoDraw(False)
            win.flip()
            continueRoutine = False
            break
        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()
    
        # refresh the screen
        if continueRoutine:
            win.flip()    
def feedback():
    global correct_answer
    global keys
    t = 0
    routine_time.reset()
    routineTimer.reset()
    routineTimer.add(S_DUR)
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = routine_time.getTime()
        # *image_wrong* updates if wrong answer:
        if t >= 0.0 and t < S_DUR and correct_answer==0:
            image_wrong.setAutoDraw(True)
        
        elif t >= 0.0 and t < S_DUR and keys==False:
            image_wrong.setAutoDraw(True)
        
        else:
            image_correct.setAutoDraw(True)
        
        if t>= S_DUR:
            image_wrong.setAutoDraw(False)
            image_correct.setAutoDraw(False)
            win.flip()
            continueRoutine = False
            break
            
        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()
            
        # refresh the screen
        if continueRoutine:
            win.flip()
    image_wrong.setAutoDraw(False)
    image_correct.setAutoDraw(False)
    win.flip()
def reset_status():
    global matrix1_started
    global matrix2_started
    global matrix3_started
    global matrix4_started
    global matrix5_started
    global matrix6_started
    global probe_started
    matrix1_started = False
    matrix2_started = False
    matrix3_started = False
    matrix4_started = False
    matrix5_started = False
    matrix6_started = False
    probe_started = False
def run_experiment():
    #This function includes the experiment definition.
    #The different routines run in the order:
    #-Instruction slide
    #-Press space bar
    #-Block instruction (wm2 or wm6)
    #-Press space bar
    #-Training block 1 (wm2)
    #-BLock instruction (wm6)
    #-Press space bar
    #-Training block 2 (wm6)
    #-After training instruction
    #-Press space bar
    #-Block instruction (wm2 or wm6 depending on the first load)
    #-Press space bar
    #-Main block 1
    #-Block instruction (wm2 or wm6 depending on the first load)
    #-Press space bar
    #-Main block 2
    #-Block instruction (wm2 or wm6 depending on the first load)
    #-Press space bar
    #-Main block 3
    #-Block instruction (wm2 or wm6 depending on the first load)
    #-Press space bar
    #-Main block 4
    
    global first_load
    #------FIRST TRAINING BLOCK--------------------------------------
    #set load in log file (2 or 6):
    set_load('WM2')
    
    #set block in log file:
    set_block('training_block_1')
  
    #run first instruction slide:
    first_instruction()
    
    #Wait for participant to press space:
#     press_key()
    
    #Show block instruction: 
    show_instruction(2)
    
    #Wait for participant to press space:
#     press_key()
    
    #Run fixation cross-targets-probe-feedback 6 times:
    for trial in range(6):
        # Show fixation cross:
        fixation_cross()
        #run trial: 
        WM2()
        #run feedback:
        feedback()
    
    
    #Load setting for next block:
    next_block()
    #-----------SECOND TRAINING BLOCK---------------------------------
    #(See comments from first training block)
    set_load('WM6')
    set_block('training_block_2')
    show_instruction(6)
#     press_key()

    for trial in range(6):
        fixation_cross()
        WM6()
        feedback()
    instruction_after_training()
    next_block()
#     press_key()
    #---------------------MAIN BLOCKS-----------------------------------------------------
    if first_load == 2:
        
        #MAIN BLOCK 1--------------------------------------------:
        set_load('WM2')
        set_block('main_block_1')
        
        show_instruction(2)
        
#         press_key()
        
        for trial in range(12):
            fixation_cross()
            WM2()
        next_block()
        
        #MAIN BLOCK 2--------------------------------------------:
        set_load('WM6')
        set_block('main_block_2')
        
        show_instruction(6)
        
#         press_key()
        
        for trial in range(12):
            fixation_cross()
            WM6()
        next_block()
        
        #MAIN BLOCK 3--------------------------------------------:
        set_load('WM2')
        set_block('main_block_3')
        
        show_instruction(2)
        
#         press_key()
        
        for trial in range(12):
            fixation_cross()
            WM2()
        next_block()
        
        #MAIN BLOCK 4--------------------------------------------:
        set_load('WM6')
        set_block('main_block_4')
        
        show_instruction(6)
        
#         press_key()
        
        for trial in range(12):
            fixation_cross()
            WM6()
        
    else: #(if first load = 6)
        #MAIN BLOCK 1--------------------------------------------:
        set_load('WM6')
        set_block('main_block_1')
        
        show_instruction(6)
        
#         press_key()
        
        for trial in range(12):
            fixation_cross()
            WM6()
        next_block()
        
        #MAIN BLOCK 2--------------------------------------------:
        set_load('WM2')
        set_block('main_block_2')
        
        show_instruction(2)
        
#         press_key()
        
        for trial in range(12):
            fixation_cross()
            WM2()
        next_block()
        
        #MAIN BLOCK 3--------------------------------------------:
        set_load('WM6')
        set_block('main_block_3')
        
        show_instruction(6)
        
#         press_key()
        
        for trial in range(12):
            fixation_cross()
            WM6()
        next_block()
        
        #MAIN BLOCK 4--------------------------------------------:
        set_load('WM2')
        set_block('main_block_4')
        
        show_instruction(2)
        
#         press_key()
        
        for trial in range(12):
            fixation_cross()
            WM2()
        
    #------END BLOCK------------------------------------
    #Show last instruction text:
    show_instruction('end')
 
#----------------------------------------------------------------------------
initialize_components()
run_experiment()
close_log_file()
win.close()
core.quit()