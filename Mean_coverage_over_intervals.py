#!/usr/bin/env Python

Usage = """
Usage:
 Mean_coverage_over_intervals.py filename1.coverage filename2.coverage filename3.coords 

filename1.coverage and filename2.coverage have three columns with chrom name, coord, and expression library coverage.
filename3.coords is list of 5' end coordinates.
    
"""

import sys
import numpy as np
import pandas as pd
window_size=100

if len(sys.argv)<4:
    print Usage
else:
    InFileName1= sys.argv[1]
    InFile1 = open(InFileName1,'r')
    OutFileNameBasis=sys.argv[1]
    OutFileNameList = OutFileNameBasis.split('_')
    OutFileName1=OutFileNameList[0]+'_'+OutFileNameList[4]+'_expr_Feb2017_summed_coverage_in_replicates'+'.txt'
    OutFileName2=OutFileNameList[0]+'_'+OutFileNameList[4]+'_expr_coverage_before_and_after_min5collapsed_5prime_ends'+'.txt'
    OutFile1 = open(OutFileName1,'w')
    OutFile2 = open(OutFileName2,'w')



    #read in a tab-delimited file with no headers where columns are chrom name, coord, and coverage
    myDF1 = pd.read_table(InFile1,names=['chrom','coord','coverage'],dtype={'coverage':np.float64})

    InFile1.close()

    InFileName2= sys.argv[2]
    InFile2 = open(InFileName2,'r')

    #read in a replicate tab-delimited file with no headers where columns are chrom name, coord, and coverage
    myDF2 = pd.read_table(InFile2,names=['chrom','coord','coverage'],dtype={'coverage':np.float64})

    InFile2.close()

    #merge into a new DF that has summed coverage values and doesn't have chorm name column
    mergedDF = pd.merge(myDF1,myDF2, how='outer', on='coord',suffixes=['_1','_2'])
    mergedDF['coverage'] = mergedDF['coverage_1']+mergedDF['coverage_2']
    summedDF = mergedDF[['coord','coverage']]

    OutFile1.write(summedDF.to_csv(sep="\t",index=False))

    InFileName3= sys.argv[3]
    InFile3 = open(InFileName3,'r')

    #read in a file that has list of coordinates (header=coord) and another column filled with 'yes' (header=Boolean)
    coordlist = pd.read_table(InFile3)

    #Add coordlist to dataframe
    summedDF = pd.merge(summedDF,coordlist, how='outer',on='coord')

    #add new column for coverage in the window after the coord of interest (incudes coord of interest as the first position in the window)
    summedDF['after_coverage']='NA'
    summedDF.loc[summedDF['Boolean']=='yes','after_coverage']=pd.rolling_mean(summedDF.coverage, window = window_size, center=True).shift(window_size/-2)

    #add new column for coverage in the window before the coord of interest (excludes coord of interest)
    summedDF['before_coverage']='NA'
    summedDF.loc[summedDF['Boolean']=='yes','before_coverage']=pd.rolling_mean(summedDF.coverage, window = window_size, center=True).shift(window_size/2)

    #delete Boolean column
    del summedDF['Boolean']

    #make a DF that includes only coords from coordlist
    coordlistDF = summedDF[summedDF.after_coverage != 'NA']

    OutFile2.write(coordlistDF.to_csv(sep="\t",index=False))

    
    
        
 

    
    
