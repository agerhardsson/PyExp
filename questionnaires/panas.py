#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from psychopy import visual, core, event

# Text settings ----------------------------------------------------------------

def panas(win, language='swedish', time='moment', textheight=0.04, textcol = 'white'):
    win = win
    language = language # swedish or english
    timeinstr = time # moment, today, pastfewdays, week, pastfewweeks, year, general
    textcol = textcol
    height = textheight # text height
    pos_vertical = 0.6
    pos_horizontal = -0.3
    space = 1.8

    # --------------------------------------------------------------------------

    timeinstr_swe = {'moment': u'du känner dig just nu.',
                     'today': u'du har känt dig idag.',
                     'pastfewdays': 'du har känt dig under de senaste dagarna.',
                     'week': 'du har känt dig under den senaste veckan.',
                     'pastfewweeks': 'du har känt dig under de senaste veckorna.',
                     'year': 'du har känt dig under det senaste året.',
                     'general': 'du generellt har känt dig, alltså, hur du känner dig i gemonsnitt.'}
    timeinstr_eng = {'moment': 'you feel this way right now, that is, at the present moment.',
                     'today': 'you have felt this way today.',
                     'pastfewdays': 'you have felt this way during the past few days.',
                     'week': 'you have felt this way during the past week.',
                     'pastfewweeks': 'you have felt this way during the past few weeks.',
                     'year': 'you have felt this way during the past year.',
                     'general': 'you generally feel this way,that is, how you feel on the average.'}

    instruction_swe = (u'Den här skalan består av ett antal ord som beskriver känslor och stämningsläge.\n\n' + u'Ange i vilken utsträckning de passar in på hur ' + timeinstr_swe[timeinstr] + '\n\n' +
    u'Det gör du genom att läsa varje ord och ange det svarsalternativ, på raden till höger, som du tycker stämmer bäst in på dig.\n\n' +
    u'Svara genom att klicka med musen. \n\n Tryck mellanslag för att gå vidare.')

    instruction_eng = ('This scale consists of a number of words that describe different feelings and emotions.\n\n' +
    'Read each item and then mark the appropriate answer in the space next to that word.\n\n'
    'Indicate to whatextent ' + timeinstr_eng[timeinstr] + '\n\n' +
    'Use the following scale to record your answers.' + '\n\n' +
    'Indicate your answer by clicking with the mouse. \n\n Press space to continue.')

    options_swe = [u'Inte alls',u'Lite',u'I någon\n  mån',u'Ganska\n  bra',
                    u'Väldigt\n  mycket']

    options_eng = [u'very slightly\n or not at all',u'a little',u'moderatly',
                    u'quite a bit',u'extremely']

    items_swe =  [u'Intresserad', u'Ivrig, upphetsad',u'Förtvivlad',u'Upprörd',
                     u'Stark', u'Entusiastisk',u'Stolt',u'Haft skuldkänslor',
                     u'Rädd',u'Fientlig',u'Pigg, vaken',u'Retlig',u'Inspirerad',
                     u'Beslutsam',u'Uppmärksam',u'Skamsen',u'Nervös',u'Skrämd',
                     u'Aktiv',u'Pirrig, ängslig']

    items_eng = ['Interested','Excited','Distressed','Upset','Strong',
                     'Enthusiastic','Proud','Guilty','Afraid','Hostile','Alert',
                     'Irritable','Inspired','Determined','Attentive',
                     'Ashamed','Nervous','Scared','Active','Jittery',]

    if language == 'swedish':
        qtext = items_swe
        otext = options_swe
        itext = instruction_swe
    elif language == 'english':
        qtext = items_eng
        otext = options_eng
        itext = instruction_eng

    h = height
    quest = []
    clist = []
    options = []
    values = []
    pos_h = pos_horizontal
    pos_v = pos_vertical


    instr = visual.TextStim(win,
                                 text=itext,
                                 pos=(pos_h-0.2, 0.03),
                                 wrapWidth=1,
                                 alignHoriz='left',
                                 height=0.06,
                                 color=textcol)

    for t in range(0,len(qtext)):

        q_stim = visual.TextStim(win,
                                    text=qtext[t],
                                    pos=(pos_h, pos_v),
                                    alignHoriz='left',
                                    height=h,
                                    color=textcol)
        pos_v = pos_v-h*space
        quest.append(q_stim)

    pos_v = pos_vertical*1.15
    pos_h = pos_horizontal + 0.3

    for t in range(0,len(otext)):
        o_stim = visual.TextStim(win,
                                    text=otext[t],
                                    pos=(pos_h, pos_v),
                                    alignHoriz='center',
                                    height=h-0.01,
                                    color=textcol)

        pos_h = pos_h+0.12
        options.append(o_stim)
    pos_v = pos_vertical
    pos_h = pos_horizontal + 0.54
    scale = []
    marker = visual.Circle(win,
                              radius=height/2,
                              lineWidth=1.8,
                              lineColor=textcol
                               )
    for r in range(0, len(qtext)):
        rs = visual.RatingScale(win, marker=marker, markerColor=textcol,
                                scale=None, low=1, high=5, showAccept=False,
                                pos=(pos_h, pos_v), lineColor=None,
                                size = 0.5, stretch=1.6, labels=None, skipKeys=None)
        pos_v = pos_v-h*space
        scale.append(rs)

    pos_v = pos_vertical
    for t in range(0, len(qtext)):
        pos_h = pos_horizontal + 0.3
        for v in range(0, len(otext)):
            v_stim = visual.TextStim(win,
                                        text=str(v+1),
                                        pos=(pos_h, pos_v),
                                        alignHoriz='center',
                                        height=h,
                                        color=textcol)
            pos_h = pos_h+0.12
            values.append(v_stim)
        pos_v = pos_v-h*space

        # ----------------------------------------------------------------------

    while not event.getKeys(keyList=['space','escape']):
        instr.draw()
        win.flip()
        if event.getKeys(keyList=['escape']):
            core.quit()

    rating = []
    for s in range(0, len(scale)):
        rating.append(str(scale[s].getRating()))

    while "None" in rating:
        rating = []
        for q in range(0, len(quest)):
            quest[q].draw()
        for o in range (0, len(options)):
            options[o].draw()
        for s in range(0, len(scale)):
            scale[s].draw()
        for v in range(0, len(values)):
            values[v].draw()
        for s in range(0, len(scale)):
            rating.append(str(scale[s].getRating()))

        if event.getKeys(keyList=['escape']):
            core.quit()

        win.flip()

    # return rating
    rating_dict = dict(zip(items_eng, rating))
    return rating_dict
    win.flip()

# -- Demo ----------------------------------------------------------------------
### Comment out to test ###

# win = visual.Window()
# panas = panas(win, 'english', 'today')
#
# print(panas)
