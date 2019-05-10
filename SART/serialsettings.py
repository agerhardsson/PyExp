                #print(ser.read(3))
                theseKeys_2 = ser.read(3)
                print(theseKeys_2)
                if "escape" in theseKeys_2:
                endExpNow = True
                if len(theseKeys_2) > 0:    
                continueRoutine = False