# Author: Lei Wang
# Date: 11/09/2018
# EECS 730
# homework 2

# Bioinformatics
### TODO:
1. Parse the HMM file
2. Construct the parameters for Viterbi algorithm
3. Compile Viterbi algorithm and return the score

### TO RUN:
command: python main.py <.hmm file> <.fasta file>

### OUTOUT:
The output contains the highest probability score of the sequence
The sequence of the profile HMM
Used ‘+’ to indicate a positive match if the emission probability of the matched character
(in the target) in the matched state is higher than the background frequency of the matched character.

