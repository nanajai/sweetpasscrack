import pandas as pd
import numpy as np
import sys
import csv
import codecs
import string
from random import randint

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
def get_struct_map(passList):
    freqMap = {}
    for password in passList:
        struct = deriveStructure(password)
        if struct in freqMap:
            freqMap[struct] += 1
        else:
            freqMap[struct] = 1
    return freqMap


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



def guess_password(sweetwords):
    print("Sweetwords set: ", sweetwords)
    sweetwords_list = sweetwords.split(',')
    pass_dict = get_rockyou_pass(sweetwords_list)
    print("pass_dict: ", pass_dict)
    
    struct_map = get_struct_map(get_100_passwords())
    print("struct_map: ", struct_map)

    highestRank = sorted(pass_dict.values())[0]
    if(highestRank != 101):
        for key,value in pass_dict.items():
                if(value == highestRank):
                    print(key)
                    return
    else: #look at another option
        print('No match to RockYou top 100 found. Searching structurally.')
        sweetwords_struct_map = {}
        
        # Create list of structures
        sweetword_structs = {}
        for sweetword in pass_dict.keys():
            struct = deriveStructure(sweetword)
            freq = 0
            if struct in struct_map:
                freq = struct_map[struct]
            ## TODO: What if the structure of the sweetword isn't in the struct_map?
            sweetword_structs[sweetword] = freq
        
        # Get the sweetwords with the most freq structures in a list.
        # Output one of them at random -- they are flat.
        print(sweetword_structs)
        topFreq = sorted(sweetword_structs.values())[-1]
        mostFreq = []
        for sWord,freq in sweetword_structs.items():
            if freq == topFreq:
                mostFreq.append(sWord)
        print(mostFreq[randint(0, len(mostFreq)-1)])
        return


def main():
    num_sets = int(sys.argv[1])
    num_sweetwords = int(sys.argv[2])
    i_name = sys.argv[3]

    with open(i_name, 'r') as i:
        for line in i:
            if line == '' or line == '\n': break
            newline = line.rstrip()
            guess_password(newline)
    i.close()


if __name__ == '__main__':
    main()
