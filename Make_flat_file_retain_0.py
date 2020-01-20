#!/usr/bin/env Python

Usage = """
Usage:
 Make_flat_file_retain_0.py filename1A.coverage filename1B.coverage filename1C.coverage filename2A.coverage filemame2B.coverage filemame2C.coverage outfilename.txt

Coverage files have three columns with chrom name, coord, and coverage.
1A,1B,1C are replicates from strain/condition 1, and 2A-2C are replicates from strain/condition 2.
    
"""


import os
import sys

# For reading through a text file line by line

if len(sys.argv)<8:
    print Usage
else:
    OutFileName = sys.argv[7]
    OutFile = open(OutFileName,'w')
    FileList = sys.argv[1:7]
    FileNum = 0
    MasterList=[]
    for FileName in FileList:
        InFile = open(FileName, 'r')
        LineNumber = 0
        RecordNum = 0
        for Line in InFile:
            Line = Line.strip('\n')
            if FileNum == 0:
                ElementList = Line.split('\t')
                MasterList.append(ElementList[1]+'\t'+ElementList[2])
            else:
                ElementList = Line.split('\t')
                MasterList[RecordNum] += '\t'+ElementList[2]
                RecordNum += 1
            LineNumber += 1
        InFile.close()
        FileNum += 1
    for Item in MasterList:
        print>>OutFile, Item
    OutFile.close()
        
 
