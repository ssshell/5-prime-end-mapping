#!/usr/bin/env Python

Usage = """
Usage:
 Collapsing_peaks_highest_in_5.py filename1
 File should have the following columns: Coord mock_1 mock_2 mock_3 phos_1 phos_2 phos_3 mean_mock_coverage mean_phos_coverage phos_over_mock log2_phos_over_mock

    
"""

import sys
import numpy as np
import pandas as pd

threshold = 5

if len(sys.argv)<2:
    print Usage
else:
    InFileName1= sys.argv[1]
    InFile1 = open(InFileName1,'r')
    OutFileNameBasis=sys.argv[1]
    OutFileNameList = OutFileNameBasis.split('.')
    OutFileName1=OutFileNameList[0]+'_marked_for_collapse_highest_in_5.txt'
    OutFileName2=OutFileNameList[0]+'_marked_for_collapse__highest_in_5_min5reads_mock_or_phos.txt'
    OutFileName3=OutFileNameList[0]+'_collapsed__highest_in_5_min5reads_mock_or_phos.txt'
 
    OutFile1 = open(OutFileName1,'w')
    OutFile2 = open(OutFileName2,'w')
    OutFile3 = open(OutFileName3,'w')
 


    #read in a tab-delimited file with headers, converting coverage columns to floats. First column will be ints.
    #Columns are: Coord mock_1 mock_2 mock_3 phos_1 phos_2 phos_3 mean_mock_coverage mean_phos_coverage phos_over_mock log2_phos_over_mock
    myDF1 = pd.read_table(InFile1)
    
    InFile1.close()

    #make a new column that indicates whether a coord has the highest coverage in a 5-nt window in mean phos library coverage
    myDF1['highest_in_5'] = (
                                   ((myDF1.mean_phos_coverage > np.roll(myDF1.mean_phos_coverage,-1)) | (myDF1.mean_phos_coverage == np.roll(myDF1.mean_phos_coverage,-1))) &
                                   ((myDF1.mean_phos_coverage > np.roll(myDF1.mean_phos_coverage,-2)) | (myDF1.mean_phos_coverage == np.roll(myDF1.mean_phos_coverage,-2))) &
                                   ((myDF1.mean_phos_coverage > np.roll(myDF1.mean_phos_coverage,+1)) | (myDF1.mean_phos_coverage == np.roll(myDF1.mean_phos_coverage,+1))) &
                                   ((myDF1.mean_phos_coverage > np.roll(myDF1.mean_phos_coverage,+2)) | (myDF1.mean_phos_coverage == np.roll(myDF1.mean_phos_coverage,+2))) 
                                    )
     
    OutFile1.write(myDF1.to_csv(sep="\t",index=False))

    #make a new DF that includes only rows in which mean phos coverage is >=5 or mean mock coverage is >=5
    myDF1['mock_or_phos_at_least_5'] = ((
    	(myDF1.mean_phos_coverage >= threshold) 
    	| 
    	(myDF1.mean_mock_coverage >= threshold) ))
    
    myDF2 = pd.DataFrame(myDF1[(myDF1.mock_or_phos_at_least_5 == True)])

    OutFile2.write(myDF2.to_csv(sep="\t",index=False))

    #make a new DF that represents the "collapsed" version of myDF2
    collapsed_DF = pd.DataFrame(myDF2[(myDF2.highest_in_3 == True)])

    OutFile3.write(collapsed_DF.to_csv(sep="\t",index=False))
    
