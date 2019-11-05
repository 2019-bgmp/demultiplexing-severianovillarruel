#!/usr/bin/env python3

'''
DEMULTIPLEXING SCRIPT (RELIES ON FUNCTIONS IN DEMULTI_FUNCTIONS FILE)
'''

import gzip
import argparse
from demulti_functions import *

def get_args():
    parser = argparse.ArgumentParser(description="files for demultiplexing")
    parser.add_argument("-i1", "--index1_file", help="path to index 1 file", required=True, type = str)
    parser.add_argument("-i2", "--index2_file", help="path to index 2 file", required=True, type = str)
    parser.add_argument("-r1", "--read1_file", help="path to read 1 file", required=True, type = str)
    parser.add_argument("-r2", "--read2_file", help="path to read 2 file", required=True, type = str)
    return parser.parse_args()

#OPEN REFERENCE INDEXES FILE, INDEX 1 FILE, INDEX 2 FILE, FORWARD SEQS FILE, REVERSE SEQS FILE
args = get_args()
INDEX_1_READS = gzip.open(args.index1_file, "rt")
INDEX_2_READS = gzip.open(args.index2_file, "rt")
FORWARD_READS = gzip.open(args.read1_file, "rt")
REVERSE_READS = gzip.open(args.read2_file, "rt")

INDEX_1_READ = []
INDEX_2_READ = []
FORWARD_READ = []
REVERSE_READ = []

poor_quality_counter = 0
hopped_counter = 0
matched_counter = 0

#MAKE A LIST WITH THE FOUR LINES OF A READ AS THE ITEMS
while(True):
    INDEX_1_READ.append(INDEX_1_READS.readline().strip()) #HEADER [0]
    INDEX_1_READ.append(INDEX_1_READS.readline().strip()) #SEQ [1]
    INDEX_1_READ.append(INDEX_1_READS.readline().strip()) #QHEADER [2]
    INDEX_1_READ.append(INDEX_1_READS.readline().strip()) #QSCORE [3]

    #grab current R2 record
    INDEX_2_READ.append(INDEX_2_READS.readline().strip())
    INDEX_2_READ.append(INDEX_2_READS.readline().strip())
    INDEX_2_READ.append(INDEX_2_READS.readline().strip())
    INDEX_2_READ.append(INDEX_2_READS.readline().strip())

    #grab current R3 record
    FORWARD_READ.append(FORWARD_READS.readline().strip())
    FORWARD_READ.append(FORWARD_READS.readline().strip())
    FORWARD_READ.append(FORWARD_READS.readline().strip())
    FORWARD_READ.append(FORWARD_READS.readline().strip())

    #grab current R4 record
    REVERSE_READ.append(REVERSE_READS.readline().strip())
    REVERSE_READ.append(REVERSE_READS.readline().strip())
    REVERSE_READ.append(REVERSE_READS.readline().strip())
    REVERSE_READ.append(REVERSE_READS.readline().strip())

    #MAKE SURE THERE NO BLANK LINES FROM OPIGINAL FILES ARE BEING READ
    if INDEX_1_READ[0] != '':

        #WRITE INDEXS IN HEARDER OF FORWARD AND REVERSE READS
        FORWARD_READ[0] = FORWARD_READ[0] + " " + INDEX_1_READ[1] + ":" + INDEX_2_READ[1]
        REVERSE_READ[0] = REVERSE_READ[0] + " " + INDEX_1_READ[1] + ":" + INDEX_2_READ[1]

        #REVERSE COMPLIMENT I2
        INDEX_2_READ[1] = rev_comper(INDEX_2_READ[1])
        
        #DEMULTIPLEX
        #Step 0. Set Conditions to None
        poor_quality_condition = None
        unknown_condition = None
        hopped_condition = None

        #Step 1. Execute functions and save, to a variable, whether the condition was met (only proceed if previous condition was not met)
        poor_quality_condition = poor_quality_reads(INDEX_1_READ,INDEX_2_READ,FORWARD_READ,REVERSE_READ)
        if poor_quality_condition != True:
            unknown_condition = unknown_reads(INDEX_1_READ,INDEX_2_READ,FORWARD_READ,REVERSE_READ)
            if unknown_condition != True:
                hopped_condition = hopped_reads(INDEX_1_READ,INDEX_2_READ,FORWARD_READ,REVERSE_READ)
                if hopped_condition != True:
                    dual_matched_condition = dual_matched_reads(INDEX_1_READ,INDEX_2_READ,FORWARD_READ,REVERSE_READ)
                    index_percentage_dict = index_percentage(INDEX_1_READ[1])
                    matched_counter += 1

        #COUNTER FOR WONKY READS
        if poor_quality_condition == True:
            poor_quality_counter += 1
        if unknown_condition == True:
            poor_quality_counter += 1
        if hopped_condition == True:
            hopped_counter += 1

    #EXIT OUT OF WHILE LOOP WHEN END OF FILE IS REACHED
    if "@" not in INDEX_1_READ[0]:
        print("Number of Reads with an Unknown Read: ", poor_quality_counter)
        print("Number of Reads an Index that Hopped: ", hopped_counter)
        print("Number of Reads with a Dual Matched Index: ", matched_counter)
        for key in index_percentage_dict:
            print("Percent of matched reads with index: ", key ," is ", ((index_percentage_dict[key]/matched_counter)*100))
        break

    #BLANK LISTS
    INDEX_1_READ = []
    INDEX_2_READ = []
    FORWARD_READ = []
    REVERSE_READ = []

INDEX_1_READS.close()
INDEX_2_READS.close()
FORWARD_READS.close()
REVERSE_READS.close()
