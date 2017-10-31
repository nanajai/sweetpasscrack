import pandas as pd
import numpy as np
import codecs
import string
import csv
import sys


def get_all_passwords():
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


#Returns a hashmap of the ranks of passwords within the top 100. It will look for the password within a sweetword
def get_rockyou_pass(sweetwords_list):

    passwords = get_all_passwords()
    pass_dict = dict.fromkeys(sweetwords_list, 101)
    print(pass_dict)
    for sweetword in sweetwords_list:
        print("Sweetword {}",sweetword)
        for i,password in enumerate(passwords):
            if(password in sweetword):
                print(password)
                pass_dict[sweetword] = i
                break

    return pass_dict





def guess_password(sweetwords):
    print("This is sweetwords {}",sweetwords)
    sweetwords_list = sweetwords.split(',')
    pass_dict = get_rockyou_pass(sweetwords_list)

    print(pass_dict)

    highestRank = sorted(pass_dict.values())[0]
    if(highestRank != 101):
        for key,value in pass_dict.items():
                if(value == highestRank):
                    print(key)
                    return
    else: #look at another option
        return 'no password' #for now





def main():
    num_sets = int(sys.argv[1])
    num_sweetwords = int(sys.argv[2])
    i_name = sys.argv[3]

    with open(i_name, 'r') as i:
        for line in i:
            if line == '' or line == '\n': break
            newline = line.rstrip()
            sweetwords = guess_password(newline)
    i.close()


if __name__ == '__main__':
    main()
