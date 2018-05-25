
def fixation_cross(start, duration, delay):

    from psychopy import core

    fixationCross = visual.TextStim(win, text=u"+", height=0.08)

    if duration == 0:
        fixationCross.setAutoDraw(True)
        win.flip()

    elif duration < 0:
        while continueRoutine:
            fixationCross.draw()
            win.flip()

            if core.CountdownTimer() < 0:
                win.flip()
                ISI.start(fxc_delay)
                ISI.complete()
                continueRoutine = False

                # check for quit (the Esc key)
            elif event.getKeys(keyList=["escape"]):
                    core.quit()
# Testar att se om jag ändrar något när
# Och nu då?
