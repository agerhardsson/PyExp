#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from future.utils import python_2_unicode_compatible
from psychopy import core
import os
import sys

instText = dict()

instText['sartintro'] = """

I det här testet kommer du få se en siffra (1-9).
Den kommer att visas en kort stund i mitten av skärmen.

Siffran följs av en ikryssad cirkel.

Din uppgift är att trycka med pekfingret för alla siffror UTOM siffran 3.

Svara så snabbt och korrekt som möjligt.

(Tryck <mellanslag> för att fortsätta)

"""

instText['probeintro'] = """


Under testets gång kommer du då och då bli avbruten med frågor om
i vilken grad du var fokuserad på uppgiften och hur medveten du var om det.

Du svarar genom att flytta markören till
höger <L> eller vänster <A>
och bekräftar ditt svar med <mellanslag>.
"""

instText['training'] = """

Du kommer nu att få göra en kortare träningsomgång av uppgiften.

Under denna träningsomgång får du feedback i form av
ett rött kryss när du svarar fel.
Dvs. när du trycker på siffran 3,
eller inte trycker på någon av de andra siffrorna.

Svara så snabbt och korrekt som möjligt.

(Tryck <mellanslag> för att starta)

"""

instText['training2'] = """

Bra. Nu fortsätter träningen, fast denna gång utan feedback.

Svara så snabbt och korrekt som möjligt.

(Tryck <mellanslag> för att starta)

"""


instText['task'] = """


Nu startar det riktiga testet.

Din uppgift är att trycka med pekfingret för alla siffror UTOM siffran 3.

Svara så snabbt och korrekt som möjligt.

(Tryck <mellanslag> för att starta)


"""

instText['continue'] = """

Tryck <mellanslag> för att fortsätta

"""

instText['end'] = """

Nu är det här testet slut, tack!

Tryck på valfri knapp för att avsluta.

"""


class instructions():

    def __init__(self, window, text_size=0.07,
                 wrapWidth=1.8, color='white',
                 folderName='instructions',
                 key=['space'], waitAfter=0.5):
        self.tSize = text_size
        self.wrapWidth = wrapWidth
        self.color = color
        self.dir = folderName
        self.win = window
        self.key = key
        self.waitAfter = waitAfter

    def load_instructions(self):
        self.path = os.getcwd()
        instructionTextsDict = instText

#        directory = self.path + '/' + self.dir + '/'
#
#        instructionTextsDict = {}
#        for file in os.listdir(directory):
#            instr = file
#            name = file[:-4]
#            with open(directory + instr, 'r') as myfile:
#                if sys.version_info[0] >= 3:
#                    text = str(myfile.read())  # for python3
#                else:
#                    text = unicode(myfile.read(), 'UTF-8')  # for python2
#                instructionTextsDict[name] = text

        return instructionTextsDict

    def start(self, instr):
        from psychopy import visual, event
        self.instr = instr
        self.win.setMouseVisible(False)
        event.clearEvents(eventType='keyboard')

        instruction_object = visual.TextStim(
            win=self.win,
            text='',
            alignText='center',
            font=u'Arial',
            height=self.tSize,
            wrapWidth=self.wrapWidth,
            color='white')

        instruction_texts = self.load_instructions()

        instruction_object.setText(instruction_texts[self.instr])

        while not event.getKeys(keyList=self.key):
            instruction_object.draw()
            self.win.flip()
            if event.getKeys(keyList=['escape']):
                core.quit()
        core.wait(0.3)
        self.win.flip()
        core.wait(self.waitAfter)


# Example --------------------------------------------------
# from psychopy import visual
# win = visual.Window()
#
# instruction = instructions(win)
# instruction.start('end')
