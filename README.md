# Demultiplexing

The "demulti_script.py" script will demultiplex reads coming from a multiplexed sequencing run.

To run the script four parameters need to be added:

-i1 :index1_reads.gz file

-i2 :index1_reads.gz file

-r1 :forward_reads.gz file

-r2 :reverse_reads.gz file


A summary of the demultiplexing will be provided in standard output

*Before running this script it is important to create an empty directoy named "demulti_files" in the directory the script is run in. Outputted reads will de placed in this directory according to the barcode associated with them.

example run: ./demulti_script.py -i1 index1.fastq.gz -i2 tindex2.fastq.gz -r1 forward_reads.fastq.gz -r2 reverse_reads.fastq.gz
