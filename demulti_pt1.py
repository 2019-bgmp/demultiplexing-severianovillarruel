#!/usr/bin/env python3
import numpy as np
import argparse
import gzip
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser(description="A program to introduce yourself")
    parser.add_argument("-i", "--input_file", help="Input file", required=True)
    parser.add_argument("-p", "--plot_name", help="Input file", type=str, required=True)
    return parser.parse_args()

args = get_args()

sum_scores = []
avg_scores = []
INPUT_FILE = args.input_file
plt_filename = args.plot_name

INPUT_FILE = gzip.open(INPUT_FILE, "rt")

#CREATE A COVERT PHRED FUNCTION
def convert_phred(letter):
    """Converts a single character into a phred score"""
    return (ord(letter) - 33)


#READ IN QSCORES
line_num = 0
for line in INPUT_FILE:
    line = line.strip()
    line_num += 1
    if line_num%4 == 0:
        asciis = line
        len_seq = len(asciis)  #use length of qscores line to initialize a list
        basepair = 0
        #MAKE ONE EMPTY ARRAY AFTER READING THE FIRST ASCII SEQ THAT WILL BE USED THROUGHOUT THE ALGORITHM
        if line_num == 4:
            for i in range(len_seq):
                sum_scores.append(0)     # [0,0,0,0,0,0,0...0]
        #EVALUATE EACH BASEPAIR AND CREATE A CUMULATIVE SUM AT EACH POSITION
        for letter in asciis:
            sum_scores[basepair] += convert_phred(letter)
            basepair += 1
#AVERAGE THE SCORE AT EACH POSITION
for score in sum_scores:
    avg_scores.append(score/(line_num/4))
print(avg_scores)


#CREATE X-AXIS POINTS
base_pair = []
for i in range(len_seq):
    base_pair.append(i)


#PLOTS
plt.plot(base_pair, avg_scores, ".")
plt.title("Distribution of QScore Averages")
plt.xlabel("Base Pair")
plt.ylabel("Mean")
plt.savefig(plt_filename)
plt.close()


INPUT_FILE.close()
