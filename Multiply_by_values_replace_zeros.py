#!/usr/bin/env Python

Usage = """
Usage:
 Multiply_by_values_replace_zeros.py text_file_name norm_factor_1 norm_factor_2 norm_factor_3 norm_factor_4 norm_factor_5 norm_factor_6

 text file has a coordinates column followed by six libraries: three replicates of two conditions
 Normalization values file has the six pre-calculated values by which each library should be multiplied.
    
"""

import sys
import numpy as np
import pandas as pd



if len(sys.argv)<8:
    print Usage
else:
    InFileName1= sys.argv[1]
    InFile1 = open(InFileName1,'r')
    OutFileNameBasis=sys.argv[1]
    OutFileNameList = OutFileNameBasis.split('_')
    OutFileName1=OutFileNameList[0]+'_'+OutFileNameList[1]+'_'+'normalized7'+'.txt'
    OutFile1 = open(OutFileName1,'w')

    #read in a tab-delimited file with headers, converting coverage columns to floats.First column will be ints.
    #First column should be coordinates, second through fourth columns replicates of condition 1, fifth through seventh columns replicates of condition 2.
    myDF1 = pd.read_table(InFile1,dtype={'mock_1':np.float64,'mock_2':np.float64,'mock_3':np.float64,'phos_1':np.float64,'phos_2':np.float64,'phos_3':np.float64})

    InFile1.close()

    norm_factor_1 = float(sys.argv[2])
    norm_factor_2 = float(sys.argv[3])
    norm_factor_3 = float(sys.argv[4])
    norm_factor_4 = float(sys.argv[5])
    norm_factor_5 = float(sys.argv[6])
    norm_factor_6 = float(sys.argv[7])
 
 #replace zero coverage values with one to make ratios meaningful
    myDF1 = myDF1.replace(to_replace=0,value=1)

 #multiply all values by normalization factor
    myDF1['mock_1'] *= norm_factor_1
    myDF1['mock_2'] *= norm_factor_2
    myDF1['mock_3'] *= norm_factor_3
    myDF1['phos_1'] *= norm_factor_4
    myDF1['phos_2'] *= norm_factor_5
    myDF1['phos_3'] *= norm_factor_6

    #Determine the mean mock coverge and mean phosphatase coverage
    myDF1 ['mean_mock_coverage'] = myDF1[['mock_1','mock_2','mock_3']].mean(axis=1)
    myDF1 ['mean_phos_coverage'] = myDF1[['phos_1','phos_2','phos_3']].mean(axis=1)

    #Determine phos/con ratio and log2 ratio
    myDF1 ['phos_over_mock'] = myDF1.mean_phos_coverage / myDF1.mean_mock_coverage
    myDF1 ['log2_phos_over_mock'] = np.log2(myDF1.phos_over_mock)

    
    OutFile1.write(myDF1.to_csv(sep="\t",index=False))
