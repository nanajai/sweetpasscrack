import pandas as pd
import numpy as np
import codecs
import string
import csv

def get_all_passwords():
    dataset = codecs.open('rockyou_password.txt', 'r', encoding='utf-8', errors='ignore')
    entries = dataset.read().split("\n")

    passwords = []

    for line in entries:
        elems = line.strip(" ").split(" ")
        if(len(elems) > 1 and elems[1] != ' '):
            passwords.append(elems[1])

    dataset.close()

    return passwords

def getPart(ch):
    if (ch.isalpha()):
        return "L"
    elif (ch.isdigit()):
        return "D"
    else:
        return "S"


#put together expression that represents password i.e. LLLLLDDD
def deriveStructure(password):
    parts = []
    for idx in range(0, len(password)):
        parts.append(getPart(password[idx]))

    return str("".join(parts))

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



def main():
    freqMap = get_struct_map(get_all_passwords())

    writer = csv.writer(open("expression_freq.csv", "w"))
    for key, val in freqMap.items():
        writer.writerow([key, val])

if __name__ == '__main__':
    main()
