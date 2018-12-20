#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import fnmatch
import os
import collections

# =============================================================================
print('''
==============================================================================
      ==============================================================
      This script lets you copy files from one directory to another
      based on information from a tab delimited list.

      Enter the full path to the directory or files you want to use.
      ==============================================================
      ''')
print('''
      From which directory would you like to copy the files?
      ''')
fromDir = input('Enter full path (From): ')
print('''
      To which directory would you like to copy the files?
      ''')
toDir = input('Enter full path (To): ')
print('''
      Which list would you like use?
      ''')
list = input('Enter full path (List): ')
print('''
      Which column name should be used from the list to match
      the files?
      ''')
match = input('Enter column name (match): ')


# =============================================================================
class copyFiles():

    def __init__(self,
                 fromDir='',
                 toDir='',
                 list='',
                 match='iaps_jpg'):

        self.fromDir = fromDir
        self.toDit = toDir
        self.list = list
        self.match = match

    def run(self, test=False):

        list_of_lists = []

        with open(self.list, 'r') as f:
            for line in f:
                inner_list = [elt.strip() for elt in line.split('\t')]
                list_of_lists.append(inner_list)
        col_names = list_of_lists[0]
        by_cols = zip(*list_of_lists[1:])

        imgDict = collections.OrderedDict()

        count = 0
        for i, col_names in enumerate(col_names):
            imgDict[col_names] = by_cols[i]
        for root, dirs, files, in os.walk(self.fromDir):
            for match in imgDict[self.match]:
                count += 1
                for fname in fnmatch.filter(files, match):
                    src_path = os.path.join(root, fname)
                    des_path = os.path.join(self.toDit, fname)
                    if os.path.exists(des_path):
                        print("File already exsists")
                        # handle it
                    print("copying '{f}' to '{d}'".format(
                        f=src_path, d=self.toDit))
                    if not test:
                        shutil.copy(src_path, self.toDit)
        print(count)


# =============================================================================
copyFiles = copyFiles(fromDir=fromDir, toDir=toDir, list=list, match=match)
copyFiles.run(test=False)  # Use test=True to check, only printing
