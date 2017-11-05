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


def get_100_passwords():
    dataset = codecs.open('rockyou_password.txt', 'r', encoding='utf-8', errors='ignore')
    entries = dataset.read().split("\n")

    passwords = []
    i = 0
    for line in entries:
        elems = line.strip(" ").split(" ")
        if(len(elems) > 1 and elems[1] != ' '):
            passwords.append(elems[1])
            i = i+1
        if(i==100):
            break

    dataset.close()

    return passwords


# Returns hashmap mapping structures to their frequencies within the top 100 most common passwords of the RockYou DB.
#def get_struct_map(passList):
#    freqMap = {}
#    for password in passList:
#        struct = deriveStructure(password)
#        if struct in freqMap:
#            freqMap[struct] += 1
#        else:
#            freqMap[struct] = 1
#    return freqMap


#Returns a hashmap of the ranks of passwords within the top 100. It will look for the password within a sweetword
def get_rockyou_pass(sweetwords_list):
    passwords = get_100_passwords()
    pass_dict = dict.fromkeys(sweetwords_list, 101)
    for sweetword in sweetwords_list:
        for i,password in enumerate(passwords):
            if(password in sweetword):
                print(password)
                pass_dict[sweetword] = i
                break

    return pass_dict

def structural_check(sweetwords_list):
    print('No discerning word frequencies found. Searching structurally.')

    #load preprocessed structure frequency map
    with open('expression_freq.csv') as f:
        struct_freq= dict(filter(None, csv.reader(f)))

    # Create list of structures
    sweetword_structs = {}
    for sweetword in sweetwords_list:
        struct = deriveStructure(sweetword)
        freq = 0
        if struct in struct_freq:
            freq = struct_freq[struct]
        ## TODO: What if the structure of the sweetword isn't in the struct_map?
        ## Sweetword has zero frequency and will be filtered out if there is any other sweetword with higher freq.
        ## If not, pass on the whole list to semantic search
        sweetword_structs[sweetword] = freq

    # Get the sweetwords with the most freq structures in a list.
    # Output one of them at random -- they are flat.
    print(sweetword_structs)
    topFreq = sorted(sweetword_structs.values())[-1]
    mostFreq = []
    for sWord,freq in sweetword_structs.items():
        if freq == topFreq:
            mostFreq.append(sWord)
    #print(mostFreq[randint(0, len(mostFreq)-1)]) ## TODO <--- CALL SEMANTIC ANALYSIS ON REMAINING LIST
    return mostFreq

def contains_english_word(sweetword):

    accumulator = Counter()
    for length in range(1,len(sweetword)+1):
        for start in range((len(sweetword)+1)-length):
            accumulator[sweetword[start:start+length]] += 1

    frequency = 0
    for subset in list(accumulator):
        if(len(subset)>2 and subset in words.words()):
            print("{} has this part of speech {}",sweetword,subset)
            frequency += 1
    return frequency




def guess_password(sweetwords):
    print("Sweetwords set: ", sweetwords)
    sweetwords_list = sweetwords.split(',')
    pass_dict = get_rockyou_pass(sweetwords_list)
    print("pass_dict: ", pass_dict)

    highestRank = sorted(pass_dict.values())[0]
    topRank = []
    for key,value in pass_dict.items():
            if(value == highestRank):
                topRank.append(key)
    if(len(topRank) == 1):
        return topRank[0]
    else:
        word_freq = {}
        for sweetword in topRank:
            print("Examining {}", sweetword)
            word_freq[sweetword] = contains_english_word(sweetword)

        #This is retrieving keys of dict in descending order of values  {ffffff, jamess, ggggg } retruns {jamess,ffffff,ggggg}
        sorted_freq = sorted(word_freq, key=word_freq.get(0), reverse=True)
        #Retrive highest freq key - jamess
        highest_freq_key = sorted_freq[0]
        #Retreive jamess corresponding value - 7 words in jamess
        highest_freq_val = word_freq[highest_freq_key]

        print("Highest Freq Val ",highest_freq_val)
        print(word_freq)
        #Check for matching freq in the rest of the words to make sure equal freq words are sent for structural test
        matching_freq_words = []
        for key,val in word_freq.items():
            if(val == highest_freq_val):
                matching_freq_words.append(key)

        if(len(matching_freq_words) == 1):
            return matching_freq_words[0]
            return
        else:
            print("Search structurally on remaining values ",matching_freq_words)
            filtered_list = structural_check(matching_freq_words)
            return filtered_list[randint(0, len(filtered_list)-1)]

def segment_edit(sweetwords):
	sweetwords_list = sweetwords.split(',')
	accumulator = Counter()

	#Find the 20 most common substrings in the string made by concatenating sweetwords
	text = ''
	for i in sweetwords_list:
		text += i

	for length in range(1,len(text)+1):
	    for start in range(len(text) - length):
	        accumulator[text[start:start+length]] += 1

	csubstr = accumulator.most_common(20)

	#Find the largest common substring in the top 20 list
	max = ''
	for i in range(0, len(csubstr)):
		if (len(csubstr[i][0]) > len(max)):
			max = csubstr[i][0]

	#Find sweetwords that contain the largetst substring
	possible_pws = []
	for sweetword in sweetwords_list:
		if(max in sweetword):
			possible_pws.append(sweetword)

	#Calculate the sums of edit distances of each pair in the sweetwords list
	distances = []
	counter = 0
	sum = 0
	for pair in itertools.product(possible_pws, repeat=2):
		sum += levenshteinDistance(*pair)
		counter += 1
		if(counter == len(possible_pws)):
			distances.append(sum)
			counter = 0
			sum = 0

	#Return the first sweetword with the least edit distance difference
	#We can randomize the index since multiple sweetwords can have the same edit distance sum
	print("password:",possible_pws[distances.index(min(distances))])
	return possible_pws[distances.index(min(distances))]

#edit distance function
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_

    print(distances[-1])
    return distances[-1]


def main():
    #nltk.download()
    num_sets = int(sys.argv[1])
    num_sweetwords = int(sys.argv[2])
    i_name = sys.argv[3]
    output_sweetwords = []
    with open(i_name, 'r') as i:
        for line in i:
            if line == '' or line == '\n': break
            newline = line.rstrip()
            output_sweetwords.append(guess_password(newline))
    i.close()

    print(','.join(output_sweetwords))

if __name__ == '__main__':
    main()
