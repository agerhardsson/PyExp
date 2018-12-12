#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import string
from psychopy import event, visual


'''
To do:
- create write to file
- create overwrite protection
- turn into class
'''

expInfo = {}
expInfo['date:'] = time.strftime("%Y-%m-%d")
expInfo['time:'] = time.strftime("%H:%M")

labels = [('Enter Subject id:', 'subject_id'),
          ('Enter version number:', 'version'),
          ('Enter seession:', 'session')]

win = visual.Window()
stim = {}
stim['label'] = visual.TextStim(
    win=win,
    text='',
    font=u'Arial')
stim['input'] = visual.TextStim(
    win=win,
    pos=(0.0, -0.2),
    text='_',
    font=u'Arial')

keys = []
for i in string.ascii_lowercase:
    keys.append(i)
for i in string.digits:
    keys.append(i)


for label in labels:
    input = []
    while True:
        stim['label'].setText(label[0])
        stim['label'].setAutoDraw(True)
        win.flip()
        key = event.getKeys(keyList=keys)
        input.append(key)
        text = ''.join([y for x in input for y in x])
        stim['input'].setText(text)

        stim['input'].setAutoDraw(True)
        win.flip()

        if event.getKeys(keyList=['backspace']):
            input = []
            stim['input'].setAutoDraw(False)
            win.flip()

        if event.getKeys(keyList=['escape', 'return']):
            break
    expInfo[label[1]] = text

print(expInfo)


# ============================================================================
# Example
