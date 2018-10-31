#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gui, amp
gui = gui.GUI(expName='AMP')
expinfo = gui.start()

run = amp()
run.startexp()
