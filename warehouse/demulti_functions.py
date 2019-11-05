#!/usr/bin/env python3

'''
FUNCTIONS FOR DEMULTIPLEXING SCRIPT
'''

NUCLEOTIDE_REF_DICT = {'A':'T', 'T':'A', 'C':'G', 'G':'C', 'N':'N'}

INDEX_REF_LST = ['GTAGCGTA','CGATCGAT','GATCAAGG','AACAGCGA',
                 'TAGCCATG','CGGTAATC','CTCTGGAT','TACCGGAT',
                 'CTAGCTCA','CACTTCAC','GCTACTCT','ACGATCAG',
                 'TATGGCAC','TGTTCCGT','GTCCTAAG','TCGACAAG',
                 'TCTTCGAC','ATCATGCG','ATCGTGGT','TCGAGAGT',
                 'TCGGATTC','GATCTTGC','AGAGTCCA','AGGATAGC']

QSCORE_CUTOFF = 30

R1_FP_DICT = {}
R2_FP_DICT = {}

for index in INDEX_REF_LST:
    R1_FP = open("demulti_files/R1_{0}.fastq".format(index),"w")
    R2_FP = open("demulti_files/R2_{0}.fastq".format(index),"w")
    R1_FP_DICT[index] = R1_FP
    R2_FP_DICT[index] = R2_FP
R1_undefined = open("demulti_files/R1_undefined.fastq", "w")
R2_undefined = open("demulti_files/R2_undefined.fastq", "w")
R1_hopped = open("demulti_files/R1_hopped.fastq", "w")
R2_hopped = open("demulti_files/R2_hopped.fastq", "w")

def rev_comper(index_2):
    '''take reverse compliment of index_2 sequence'''
    index_2_rc = ''
    for nucleotide in index_2:
        if nucleotide in NUCLEOTIDE_REF_DICT.keys():
            index_2_rc += NUCLEOTIDE_REF_DICT[nucleotide]
    index_2_rc = index_2_rc[::-1]
    return index_2_rc

#OUTPUT POOR QUALITY READS
def poor_quality_reads(index_1, index_2_rc, read1, read2):
    '''identify poor quality indexes and write them out to a file'''
    for letter_index_1, letter_index_2 in zip(index_1[3],index_2_rc[3]):
        if ord(letter_index_1) - 33 < QSCORE_CUTOFF:
            R1_undefined.write('{0}\n{1}\n{2}\n{3}\n'.format(read1[0], read1[1], read1[2], read1[3]))
            R2_undefined.write('{0}\n{1}\n{2}\n{3}\n'.format(read1[0], read1[1], read1[2], read1[3]))
            # print("problem!",index_1[3], index_2_rc[3],letter_index_1,"\n")
            return True
            break
        elif ord(letter_index_2) - 33 < QSCORE_CUTOFF:
            R1_undefined.write('{0}\n{1}\n{2}\n{3}\n'.format(read1[0], read1[1], read1[2], read1[3]))
            R2_undefined.write('{0}\n{1}\n{2}\n{3}\n'.format(read1[0], read1[1], read1[2], read1[3]))
            # print("problem!",index_1[3], index_2_rc[3],letter_index_2,"\n")
            return True
            break

# OUTPUT UNKNOWN READS
def unknown_reads(index_1, index_2_rc, read1, read2):
    '''identify unknown indexes then write them out to a file'''
    if index_1[1] not in INDEX_REF_LST:
        R1_undefined.write('{0}\n{1}\n{2}\n{3}\n'.format(read1[0], read1[1], read1[2], read1[3]))
        R2_undefined.write('{0}\n{1}\n{2}\n{3}\n'.format(read1[0], read1[1], read1[2], read1[3]))
        # print("unknown read!",index_1[1], index_2_rc[1],"\n")
        return True
    elif index_2_rc[1] not in INDEX_REF_LST:
        R1_undefined.write('{0}\n{1}\n{2}\n{3}\n'.format(read1[0], read1[1], read1[2], read1[3]))
        R2_undefined.write('{0}\n{1}\n{2}\n{3}\n'.format(read1[0], read1[1], read1[2], read1[3]))
        # print("unknown read!",index_1[1], index_2_rc[1],"\n")
        return True

#OUTPUT MISMATCHED READS
def hopped_reads(index_1, index_2_rc, read1, read2):
   '''identify hopped indexes then write them out to a file'''
   if index_1[1] in INDEX_REF_LST:
       if index_2_rc[1] in INDEX_REF_LST:
           if index_1[1] != index_2_rc[1]:
              R1_hopped.write('{0}\n{1}\n{2}\n{3}\n'.format(read1[0], read1[1], read1[2], read1[3]))
              R2_hopped.write('{0}\n{1}\n{2}\n{3}\n'.format(read1[0], read1[1], read1[2], read1[3]))
              # print("hopped read!",index_1[1], index_2_rc[1],"\n")
              return True

#OUTPUT MATCHED READS
def dual_matched_reads(index_1, index_2_rc, read1, read2):
    '''identify correctly paired reads then write them out to a file'''
    if index_1[1] in INDEX_REF_LST:
        if index_2_rc[1] in INDEX_REF_LST:
            if index_1[1] == index_2_rc[1]:
                R1_FP_DICT[index_1[1]].write('{0}\n{1}\n{2}\n{3}\n'.format(read1[0], read1[1], read1[2], read1[3]))
                R2_FP_DICT[index_1[1]].write('{0}\n{1}\n{2}\n{3}\n'.format(read1[0], read1[1], read1[2], read1[3]))
                # print("matched read :) !",index_1[1], index_2_rc[1],"\n")
                return True

counter_dict = {}
def index_percentage(index_1):
    if index_1 not in counter_dict:
        counter_dict[index_1] = 1
    else:
        counter_dict[index_1] += 1
    return counter_dict
