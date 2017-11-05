import pandas as pd
import numpy as np
import sys
import csv
import codecs
import string
import itertools
from random import randint
from collections import Counter
import nltk
import operator
from nltk.corpus import words
from itertools import chain, combinations


def getPart(ch):
    if (ch.isalpha()):
        return "L"
    elif (ch.isdigit()):
        return "D"
    else: return "S"


def deriveStructure(password):
    parts = []
    for idx in range(0, len(password)):
        parts.append(getPart(password[idx]))

    return str("".join(parts))


# Returns a hashmap of the ranks of passwords within the top 100. It will look for the password within a sweetword
def get_rockyou_pass(sweetwords_list):
    passwords = []
    with open('top_pass.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter='\n')
        for row in readCSV:
            passwords.append("".join(row))


    pass_dict = dict.fromkeys(sweetwords_list, 101)
    for sweetword in sweetwords_list:
        for i,password in enumerate(passwords):
            if(password in sweetword):
                pass_dict[sweetword] = i
                break

    return pass_dict


def structural_check(sweetwords_list):

    # Load preprocessed structure frequency map from RockYou DB.
    with open('expression_freq.csv') as f:
        struct_freq= dict(filter(None, csv.reader(f)))

    # Create list of structures in sweetwords.
    sweetword_structs = {}
    for sweetword in sweetwords_list:
        struct = deriveStructure(sweetword)
        freq = 0
        if struct in struct_freq:
            freq = struct_freq[struct]
        ## else, sweetword has zero frequency and will be filtered out if there is any other sweetword with higher freq.
        sweetword_structs[sweetword] = freq

    # Get the sweetwords with the most freq structures in a list.
    topFreq = sorted(sweetword_structs.values())[-1]
    mostFreq = []
    for sWord,freq in sweetword_structs.items():
        if freq == topFreq:
            mostFreq.append(sWord)
    return mostFreq

def contains_english_word(sweetword):

    accumulator = Counter()
    for length in range(1,len(sweetword)+1):
        for start in range((len(sweetword)+1)-length):
            accumulator[sweetword[start:start+length]] += 1

    frequency = 0
    for subset in list(accumulator):
        if(len(subset)>2 and subset in words.words()):
            frequency += 1
    return frequency


def guess_password(sweetwords):
    sweetwords_list = sweetwords.split(',')
    pass_dict = get_rockyou_pass(sweetwords_list)

    highestRank = sorted(pass_dict.values())[0]
    topRank = []
    for key,value in pass_dict.items():
            if(value == highestRank):
                topRank.append(key)
    if(len(topRank) == 1):
        return sweetwords_list.index(topRank[0])
    else:
        word_freq = {}
        for sweetword in topRank:
            word_freq[sweetword] = contains_english_word(sweetword)

        sorted_freq = sorted(word_freq, key=word_freq.get(0), reverse=True)
        highest_freq_key = sorted_freq[0]
        highest_freq_val = word_freq[highest_freq_key]

        matching_freq_words = []
        for key,val in word_freq.items():
            if(val == highest_freq_val):
                matching_freq_words.append(key)

        if(len(matching_freq_words) == 1):
            return sweetwords_list.index(matching_freq_words[0])

        else:
            filtered_list = structural_check(matching_freq_words)
            return sweetwords_list.index(filtered_list[randint(0, len(filtered_list)-1)])

def main():
    num_sets = int(sys.argv[1])
    num_sweetwords = int(sys.argv[2])
    i_name = sys.argv[3]
    output_indices = []
    with open(i_name, 'r') as i:
        for line in i:
            if line == '' or line == '\n': break
            newline = line.rstrip()
            output_indices.append(guess_password(newline)+1)
    i.close()
    print(','.join([str(i) for i in output_indices]))

if __name__ == '__main__':
    main()
