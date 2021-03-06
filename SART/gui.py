#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkMessageBox
import time
import os


class GUI():

    def __init__(self, expName='', width=400, height=100):
        self.expName = expName
        self.width = width
        self.height = height

    def check_participants(self):
        self.ppt_exists = False
        ppt_count = 0
        ppt_list = []
        filename = str(self.participant)
        for file in os.listdir("data/"):
            if file.endswith(".txt"):
                ppt = file[9:-4]  # remove first 10 characters (date) and .txt
                ppt_list.append(ppt)
                for ppt in ppt_list:
                    if filename == ppt:
                        ppt_count += 1
        if ppt_count > 0:
            self.ppt_exists = True
        return self.ppt_exists

    def close_gui(self):
        self.buttonPress = 'Cancel'
        self.root.destroy()

    def start_exp(self):
        self.version = format(int(self.vers.curselection()[0] + 1), '02d')
        if self.version == '03':
            self.version = u'tr'
        self.session = format(int(self.sess.get()), '02d')
        self.participant = str(format(int(self.subj.get()), '04d') + "_" +
                               self.version + "_" +
                               self.session)
        self.mri = self.var.get()
        if self.check_participants():
            # tk.messagebox.showinfo("Warning", "Subject already exists") # P3
            tkMessageBox.showwarning("Warning",
                                     "Subject already exists for that session")
        if not self.check_participants():
            if len(self.participant) < 1:
                print('Fill in particpant')
            elif len(self.version) < 1:
                print('Fill in version')
            elif len(self.participant) > 0 and len(self.version) > 0:
                self.buttonPress = 'OK'
                self.root.destroy()

    def createBox(self):

        self.root = tk.Tk()
        self.root.attributes('-alpha', 1.0)
        self.root.title(self.expName)

        self.frame = tk.Frame(master=self.root,
                              width=self.width,
                              height=self.height)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')
        self.frame.pack()

        self.lab_subj = tk.Label(self.frame, text='Participant:')
        self.subj = tk.Entry(self.frame)
        self.lab_vers = tk.Label(self.frame, text='Version:')
        self.vers = tk.Listbox(self.frame, height=3)
        self.vers.insert(1, '1')
        self.vers.insert(2, '2')
        self.vers.insert(3, 'Training')
        self.lab_sess = tk.Label(self.frame, text='Session:')
        self.sess = tk.Entry(self.frame)
        self.var = tk.BooleanVar(value=True)
        self.lab_mode = tk.Label(self.frame, text='MRI:')
        self.mode = tk.Checkbutton(self.frame,
                                   state='active',
                                   variable=self.var,
                                   )
        self.lab_date = tk.Label(self.frame, text='Date:')
        self.date = tk.Label(self.frame, text=time.strftime("%Y-%m-%d"))
        self.lab_time = tk.Label(self.frame, text='Time:')
        self.time = tk.Label(self.frame, text=time.strftime("%H:%M"))

        self.lab_subj.grid(row=1, sticky='e')
        self.lab_vers.grid(row=2, sticky='e')
        self.lab_sess.grid(row=3, sticky='e')
        self.lab_mode.grid(row=4, sticky='e')
        self.lab_date.grid(row=5, sticky='e')
        self.lab_time.grid(row=6, sticky='e')

        self.subj.grid(row=1, column=1)
        self.vers.grid(row=2, column=1)
        self.sess.grid(row=3, column=1)
        self.mode.grid(row=4, column=1, sticky='w')
        self.date.grid(row=5, column=1)
        self.time.grid(row=6, column=1)

        self.buttonOK = tk.Button(self.frame, text='OK', state='normal',
                                  command=self.start_exp)
        self.buttonCancel = tk.Button(self.frame, text='Cancel',
                                      command=self.close_gui)

        self.buttonCancel.grid(row=7, column=0, sticky='w')
        self.buttonOK.grid(row=7, column=1, sticky='e')

        self.center(self.root)

    def center(self, win):
        """
        centers a tkinter window
        :param win: the root or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    def expInfo(self):
        if self.buttonPress == 'Cancel':
            self.input = 'User pressed cancel'
        else:
            self.input = {'date': time.strftime("%Y-%m-%d"),
                          'time': time.strftime("%H:%M:%S"),
                          'expName': self.expName,
                          'subject_id': self.participant,
                          'version': self.version,
                          'session': self.session,
                          'mri': self.mri}
        return self.input

    def start(self):
        self.createBox()
        self.root.mainloop()
        export = self.expInfo()
        return export


# Example ------------------------------------
#
# gui = GUI(expName='SART')
# ExpInfo = gui.start()
# print(ExpInfo)
