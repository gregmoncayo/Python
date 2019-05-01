#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'missingWords' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts following parameters:
#  1. STRING s
#  2. STRING t
#
lis = []
mis = []
tis = []

def missingWords(s, t):
    if (s == ""):
        return false

    if (t == ""):
        return False

    if(s.isdigit() or t.isdigit()):
        return False

    if (len(s) > 1000000):
        return False

    word = s.split()
    term = t.split()

    missing = list(set(word) - set(term))
    missing.sort(key=len)
    
    return missing
    # Write your code here

if __name__ == '__main__':
 #   fptr = open(os.environ['OUTPUT_PATH'], 'w')
    print("Enter a string: ")
    s = input()
    print("Another one: ")
    t = input()

    result = missingWords(s, t)

    fptr.write('\n'.join(result))
    fptr.write('\n')

    fptr.close()
