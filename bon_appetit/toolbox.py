#!/usr/bin/python

import sys

class Commons:
    '''Common tools class. Gael Guibon (LSIS-CNRS)'''
    name = ""
    
    def __init__(self, name):
        self.name = name
            
    def progressBar(self, value, endvalue, bar_length=100):
        '''print the progress bar given the values.
        default bar_length = 100'''
        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()

    def writeFile(self, content, pathname):
        '''write a file'''
        f = open(pathname,'w')
        f.write(content) # python will convert \n to os.linesep
        f.close() # you can omit in most cases as the destructor will call it
    
    def readFile(self, path):
        '''read a file given a path. Return the content in a string'''
        with open(path) as f:
            res = f.read()
        return res
    
    def readFileLines(self, path):
        '''read a file given a path. Return the content in a list of lines'''
        with open(path) as f:
            res = f.readlines()
        return res
    
    def str2list(self, content):
        '''transform a string content to a list of lines'''
#         buf = StringIO.StringIO(content)
#         lines = buf.readlines()
#         lines = []
# #         lines = content.readLines()
#         for s in content :
#             lines.append(s)
        lines = content.split("\n")
        return lines
    
    def chunkIt(self, seq, num):
        """Split a sequence into roughly equal parts"""
        avg = len(seq) / float(num)
        out = []
        last = 0.0
        
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        
        return out
    