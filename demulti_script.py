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
# INDEX_1 = gzip.open("args.index1_file", "r")
# INDEX_2 = gzip.open("args.index2_file", "r")
# FORWARD_READ = gzip.open("read1_file", "r")
# REVERSE_READ = gzip.open("read2_file", "r")

args = get_args()
INDEX_1_READS = open(args.index1_file, "r")
INDEX_2_READS = open(args.index2_file, "r")
FORWARD_READS = open(args.read1_file, "r")
REVERSE_READS = open(args.read2_file, "r")

INDEX_1_READ = []
INDEX_2_READ = []
FORWARD_READ = []
REVERSE_READ = []

poor_quality_counter = 0
hopped_counter = 0
matched_counter = 0

while(True):
    INDEX_1_READ.append(INDEX_1_READS.readline().strip()) #HEADER
    INDEX_1_READ.append(INDEX_1_READS.readline().strip()) #SEQ
    INDEX_1_READ.append(INDEX_1_READS.readline().strip()) #QHEADER
    INDEX_1_READ.append(INDEX_1_READS.readline().strip()) #QSCORE

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

        # print(INDEX_2_READ[1])

        #RUN READS THROUGH EACH FUNCTION IFF IT DOES NOT SATISFY THE PREVIOUS CONDITION
        #1a. POOR QUALITY CONDITION (execute function and save whether the condition was met)
        poor_quality_condition = poor_quality_reads(INDEX_1_READ,INDEX_2_READ,FORWARD_READ,REVERSE_READ)
        #1b. UNKNOWN READ CONDITION (if the previous condition was not met execute the function and save whether this condition was met)
        if (poor_quality_condition != True):
            unknown_condition = unknown_reads(INDEX_1_READ,INDEX_2_READ,FORWARD_READ,REVERSE_READ)
        if poor_quality_condition == True or unknown_condition == True:
            poor_quality_counter += 1 #add 1 to counter if either condition was met

        #2. HOPPED CONDITION (if the previous conditions were not met execute the function and save whether this condition was met)
        if (poor_quality_condition != True) and (unknown_condition != True):
            hopped_condition = hopped_reads(INDEX_1_READ,INDEX_2_READ,FORWARD_READ,REVERSE_READ)
        if hopped_condition == True:
            hopped_counter += 1 #add 1 to counter if either condition was met

        #THE REST ARE MATCHED (if the previous conditions were not the read is matched)
        if (poor_quality_condition != True) and (unknown_condition != True) and (hopped_condition != True):
            index_percentage_dict = index_percentage(INDEX_1_READ[1]) #run matched reads through a function that continuously updates a dictionary with the num of reads with each index
            dual_matched_condition = dual_matched_reads(INDEX_1_READ,INDEX_2_READ,FORWARD_READ,REVERSE_READ)
            matched_counter += 1 #add 1 to counter if read got to these lines of code

    #EXIT OUT OF WHILE LOOP WHEN END OF FILE IS REACHED
    if "@" not in INDEX_1_READ[0]:
        print("Number of Reads with an Index of Poor Quality: ", poor_quality_counter)
        print("Number of Reads an Index that Hopped: ", hopped_counter)
        print("Number of Reads with a Dual Matched Index: ", matched_counter)
        for key in index_percentage_dict:
            print("Percent of matched reads with index: ",key," is ", ((index_percentage_dict[key]/matched_counter)*100))
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
