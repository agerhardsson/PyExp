#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from psychopy import visual

from questionnaires import panas, kss

win = visual.Window(color='black')
panas = panas.panas(win, 'swedish', time='moment', textcol='white')

kss = kss.kss(win, use_mouse=True, textcol='white')

print(panas)
print(kss)
