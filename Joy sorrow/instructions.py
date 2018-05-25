#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os

def instructions():
    directory = 'instructions/'

    instruction_texts = {}
    for file in os.listdir(directory):
        instr = file
        name = file[:-4]
        with open(directory + instr, 'r') as myfile:
            text = unicode(myfile.read(), 'UTF-8')
            instruction_texts[name] = text

    return instruction_texts
