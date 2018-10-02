#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import core, parallel

# you chave to find out what's the address on your computer.. I don't remember
# how to do that but you should find the instructions when you google

p_port = parallel.ParallelPort(address="0x4020")


def trigger(trig, dur):
    p_port.setData(trig)
    core.wait(dur)  # duration of trigger
    p_port.setData(0)  # turn sound trigger off

# and then you just send a trigger with the function, for example:

# Turn ON all triggers (but if you use StimTracker, for some reason their
# triggers are invertes, so you have to keep it in mind.
# 0 would then turn OFF all triggers


trigger(255, 0.01)
