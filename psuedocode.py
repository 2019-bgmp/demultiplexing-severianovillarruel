#!/usr/bin/env python3

#OPEN REFERENCE INDEXES FILE, INDEX 1 FILE, INDEX 2 FILE, FORWARD SEQS FILE, REVERSE SEQS FILE
#open indexes reference file
#open index1 file
#open index2 file
#open forward seq read file
#open reverse seq read file

#READ IN LINES FOR REFERENCE INDEXES, INDEX1, INDEX 2, FORWARD SEQS, REVERSE SEQS
#VARIABLE ASSIGNMENT
#read in line for index reference file
#index_ref = column four
#index_ref_seq = column five

    #read in line for index 1 file
    #index1_seq = every second line
    #index1_qscore = every fourth line

        #read in line for index 2 file
        #index2_seq = every second line
        #index2_qscore = every fourth line

            #read in line for forward seqs file
            #forward_seq = every second line
            #forward_seq qscore = every fourth line

                #read in line for reverse seqs file
                #reverse_seq = every second line
                #reverse_seq qscore

#nucleotide_ref = {'A':'T', 'T':'A', 'C':'G', 'G':'C', 'N':'N'}
#REVERSE COMPLIMENT FUNCTION
# def rev_comp(index2_seq, basepairs_dict):
#     ```take reverse compliment of sequence```
#     index2_seq_rev_comp = ''
#     iterate over each index2_seq
#     convert each nucleotide to its compliment using the nucleotide_ref_dict and add it to the blank rev_comp string
#     reverse sort index2_seq_rev_comp
#     retrun index2_seq_rev_comp

#use with open("example.txt", "a") as text_file: to not overwrite outpufiles
#index_ref_dict = {index_ref_seq:index_ref}
#OUTPUT LOW QUALITY OR UNKNOWN READS
#def id_weird_reads(index1_seq, read1_seq, index2_seq_rev_comp, read2_seq, index_ref_dict):
#   ```identify index_seq that are low quality or unknown and write them out to a file```
#   iterate over each quality score in the index_seq
#   if there is a quality score lower than 33
#   1) add index1_seq and index1_ref and index2_seq and index2_ref to the header and write the forward seq out to a file called 'low_qual_and_unknown_forward'
#   2) add index1_seq and index1_ref and index2_seq and index2_ref to the header and write the reverse seq out to a file called 'low_qual_and_unknown_rev'
#   if the average quality score of seq is below 35
#   1) add index1_seq and index1_ref and index2_seq and index2_ref to the header and write the forward seq out to the 'low_qual_and_unknown_forward'
#   2) add index1_seq and index1_ref and index2_seq and index2_ref to the header and write the forward seq out to the 'low_qual_and_unknown_rev'
#   if the index is not found in the dictionary
#   1) add index1_seq and index1_ref and index2_seq and index2_ref to the header and write the forward seq out to the 'low_qual_and_unknown_forward'
#   2) add index1_seq and index1_ref and index2_seq and index2_ref to the header and write the forward seq out to the 'low_qual_and_unknown_rev'

#OUTPUT MISMATCHED READS
#def hopped_read)sort(index1_seq, read1_seq, index2_seq, read2_seq, index_ref_dict)
#   ```identify hopped indexes and write them out to a file
#   if index1_seq is a key in index_ref_dict and index2_rev_comp is a key in index_ref_dict but the index_seqs do not equal eachother
#   1) add index1_seq and index1_ref and index2_seq and index2_ref to the header and write the forward seq out to a file called 'hopped_forward'
#   2) add index1_seq and index1_ref and index2_seq and index2_ref to the header write the reverse seq out to a file called 'hopped_rev'

#OUTPUT MATCHED READS
#def dual_matched_sort(index1_seq, read1_seq, index2_seq_rev_comp, read2_seq, index_ref_dict)
#   ```identify correctly paired reads and write them out to a file
#   if index1_seq and index2_seq are keys in index_ref_dict and if index1_seq equals index2_seq and if they are above the cutoff I created
#   1) add the index_seq and index_ref to the header and write the forward read out to a file named 'forward' + the index_ref
#   2)  add the index_seq and index_ref to the header and write the reverse read out to a file named 'reverse' + the index_ref
