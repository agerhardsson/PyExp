#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


# Functions that control stimuli presentation ---------------------------------
class log():

    def __init__(self, folderName='data'):
        self.dir = folderName

    def createFile(self, dataKeys):
        self.dataKeys = dataKeys
        self.path = os.getcwd()
        self.directory = self.path + '/' + self.dir + '/'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        self.file = (self.directory +
                     self.dataKeys['Date'] + "_" +
                     self.dataKeys['subject_id'] + "_" +
                     self.dataKeys['Version'] + "_" +
                     self.dataKeys['Session'] +
                     ".txt")
        self.f = open(self.file, "w")
        for key in self.dataKeys.keys():
            self.f.write(str(key) + '\t')
        self.f.write('\n')
        self.f.close()

    def append(self, dataVals):
        self.dataVals = dataVals
        self.f = open(self.file, "a")
        for value in self.dataVals.values():
            self.f.write(str(value) + '\t')
        self.f.write('\n')
        self.f.close()
