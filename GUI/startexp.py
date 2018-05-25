import Tkinter as tk

gui = tk.Tk()
gui.attributes('-alpha', 1.0)

def close_gui():
    gui.destroy()
    print "User pressed cancel"

def start_exp():
    global participant
    global version
    participant = str(entry_1.get())
    version = str(entry_2.get())
    if len(participant) < 1:
        print "Fill in particpant"
    elif len(version) < 1:
        print "Fill in version"
    elif len(participant) > 0 and len(version) > 0:
        # print participant, version
        gui.destroy()

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

frame = tk.Frame(gui, height=100, width=200)
frame.place(relx=0.5, rely=0.5, anchor='center')
frame.pack()

label_1 = tk.Label(frame, text='Participant:')
entry_1 = tk.Entry(frame)
label_2 = tk.Label(frame, text='Version:')
entry_2 = tk.Entry(frame)

c = tk.Checkbutton(frame, text='')
c.grid(row=3,columnspan=2)

buttonOK = tk.Button(frame, text='OK', state='normal', command=start_exp)
buttonCancel = tk.Button(frame, text='Cancel', command=close_gui)

label_1.grid(row=1, sticky='e')
label_2.grid(row=2, sticky='e')

entry_1.grid(row=1, column=1)
entry_2.grid(row=2, column=1)

buttonCancel.grid(row=4, column=0, sticky='w')
buttonOK.grid(row=4, column=1, sticky='e')

center(gui)
gui.mainloop()
print participant, version
