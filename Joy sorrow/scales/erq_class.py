#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time, os
from psychopy import visual, core, event

# Text settings ----------------------------------------------------------------
class erq:
    def __init__(self,
                 win,
                 subject_id,
                 language='swedish',
                 timeinstr='moment',
                 textheight=0.05,
                 textcol='white'):
        self.win = win
        self.subject_id = subject_id
        pos_top_max = 0.9
        pos_vertical = pos_top_max - 0.12
        pos_horizontal = -0.4
        space = 1.8

        # --------------------------------------------------------------------------

        instruction_swe = (u'Den här skalan består av ett antal ord som beskriver känslor och stämningsläge.\n\n' + u'Ange i vilken utsträckning de passar in på hur '
        u'Det gör du genom att läsa varje ord och ange det svarsalternativ, på raden till höger, som du tycker stämmer bäst in på dig.\n\n' +
        u'Svara genom att klicka med musen. \n\n Tryck mellanslag för att gå vidare.')

        instruction_eng = ('This scale consists of a number of words that describe different feelings and emotions.\n\n' +
        'Read each item and then mark the appropriate answer in the space next to that word.\n\n'
        'Indicate to whatextent ' + timeinstr_eng[timeinstr] + '\n\n' +
        'Use the following scale to record your answers.' + '\n\n' +
        'Indicate your answer by clicking with the mouse. \n\n Press space to continue.')

        options_swe = [u'Samtycker\n inte alls',    # 1
                       '',                          # 2
                       '',                          # 3
                       u'Neutral',                  # 4
                       '',                          # 5
                       ''                           # 6
                        u'Samtycker\n starkt']      # 7

        options_eng = []

        items_swe =  [u'När jag vill känna mer positiva känslor inom mig\n' +
                      u' (som glädje eller munterhet), ändrar jag vad jag tänker på.', # 1
                      u'Jag behåller mina känslor för mig själv.', # 2
                      u'När jag vill känna mindre negativa känslor\n' +
                      u' (som sorg/nedstämdhet eller ilska), ändrar jag vad jag tänker på.', # 3
                      u'När jag känner positiva känslor, är jag noga med att inte visa det.', # 4
                      u'När jag befinner mig i en stressig situation, tvingar jag\n' +
                      u' mig själv att tänka på det på ett sätt som håller mig lugn.', # 5
                      u'Jag kontrollerar mina känslor genom att inte uttrycka dem.', # 6
                      u'När jag vill känna mer positiva känslor, ändrar jag på\n' +
                      u' mitt tankesätt om situationen', # 7
                      u'Jag kontrollerar mina känslor genom att ändra på mitt\n' +
                      u' tankesätt om situationen jag befinner mig i.', # 8
                      u'När jag känner negativa känslor, ser jag till att inte uttrycka dem.', # 9
                      u'När jag vill känna mindre negativa känslor, ändrar jag\n' +
                      u' på sättet jag tänker om situationen.' ] # 10

        self.items_eng = []

        if language == 'swedish':
            qtext = items_swe
            otext = options_swe
            itext = instruction_swe
        elif language == 'english':
            qtext = self.items_eng
            otext = options_eng
            itext = instruction_eng

        h = textheight
        self.quest = []
        self.options = []
        self.values = []
        pos_h = pos_horizontal
        pos_v = pos_vertical


        self.instr = visual.TextStim(self.win,
                                     text=itext,
                                     pos=(pos_h-0.2, 0.03),
                                     wrapWidth=1,
                                     alignHoriz='left',
                                     height=0.06,
                                     color=textcol)

        for t in range(0,len(qtext)):

            q_stim = visual.TextStim(self.win,
                                        text=qtext[t],
                                        pos=(pos_h, pos_v),
                                        alignHoriz='left',
                                        height=h,
                                        color=textcol)
            pos_v = pos_v-h*space
            self.quest.append(q_stim)

        pos_v = pos_top_max
        pos_h = pos_horizontal + 0.4

        for t in range(0,len(otext)):
            o_stim = visual.TextStim(self.win,
                                        text=otext[t],
                                        pos=(pos_h, pos_v),
                                        alignHoriz='center',
                                        height=h-0.01,
                                        color=textcol)

            pos_h = pos_h+0.15
            self.options.append(o_stim)
        pos_v = pos_vertical
        pos_h = pos_horizontal + 0.7
        self.scale = []
        marker = visual.Circle(self.win,
                                  radius=textheight/2,
                                  lineWidth=1.8,
                                  lineColor=textcol
                                   )
        for r in range(0, len(qtext)):
            rs = visual.RatingScale(self.win, marker=marker, markerColor=textcol,
                                    scale=None, low=1, high=5, showAccept=False,
                                    pos=(pos_h, pos_v), lineColor=None,
                                    size = 0.5, stretch=2, labels=None, skipKeys=None)
            pos_v = pos_v-h*space
            self.scale.append(rs)

        pos_v = pos_vertical
        for t in range(0, len(qtext)):
            pos_h = pos_horizontal + 0.4
            for v in range(0, len(otext)):
                v_stim = visual.TextStim(self.win,
                                            text=str(v+1),
                                            pos=(pos_h, pos_v),
                                            alignHoriz='center',
                                            height=h,
                                            color=textcol)
                pos_h = pos_h+0.15
                self.values.append(v_stim)
            pos_v = pos_v-h*space

        self.history = []
            # ----------------------------------------------------------------------
    def draw(self):
        event.clearEvents(eventType='keyboard')

        while not event.getKeys(keyList=['space','escape']):
            self.instr.draw()
            self.win.flip()
            if event.getKeys(keyList=['escape']):
                core.quit()

        rating = []
        for s in range(0, len(self.scale)):
            rating.append(str(self.scale[s].getRating()))

        while "None" in rating:
            rating = []
            rt = []
            for q in range(0, len(self.quest)):
                self.quest[q].draw()
            for o in range (0, len(self.options)):
                self.options[o].draw()
            for s in range(0, len(self.scale)):
                self.scale[s].draw()
            for v in range(0, len(self.values)):
                self.values[v].draw()
            for s in range(0, len(self.scale)):
                rating.append(str(self.scale[s].getRating()))

            if event.getKeys(keyList=['escape']):
                core.quit()
            self.win.flip()
        core.wait(0.5)
        self.win.flip()
        self.response = {}
        self.response = dict(zip(self.items_eng, rating))
        self.response['date'] = time.strftime("%d/%m/%Y")
        self.response['time'] = time.strftime("%H:%M:%S")

        self.history.append(self.response)

    def getResponse(self):
        return self.response

    def getHistory(self):
        return self.history

    def clear(self):
        self.response = {}
        self.history = []

    def logFile(self, onlyLatest=False):
        directory = 'data/erq/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = directory + str(self.subject_id) + "_erq_.txt"
        if not os.path.exists(file_path):
            f = open(file_path, "w")
            f.write('subject_id\t'
                + 'date\t'
                + 'time\t'
                + '\t'.join(self.response.keys()) + '\n'
            )
            f.close()

        f = open(file_path, "a")
        if onlyLatest==True:
            f.write(
                str(self.subject_id) + '\t'  # id
                + self.response['date'] + '\t'  # date
                + self.response['time'] + '\t'  # time
                + '\t'.join(self.response.values()) + '\n'  # answer
            )
        elif onlyLatest==False:
            for h in self.history:
                f.write(
                    str(self.subject_id) + '\t'  # id
                    + str(h['date']) + '\t'  # date
                    + str(h['time']) + '\t'  # time
                    + '\t'.join(str(h.values())) + '\n'  # answer
                )
        f.close()



# -- Demo ----------------------------------------------------------------------
### Comment out to test ###
# ppt = raw_input('Participant: ')
# win = visual.Window()
# p = erq(win, ppt, 'english', 'today')
# print p
# quit()
