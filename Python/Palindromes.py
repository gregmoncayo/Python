#!/usr/bin/env python

# Gregory Moncayo
# FSUID: glm16b
# 09/18/2018

list = []       # list that contains the Palindromes string

# Dictionary functions that adds the palindromes to the list

def dict(first):
        str1 = str(first)
        list.append(str1)
        return list

# Reverse function that reverses the string that was entered

def reverse(r):
        return r[::-1]

# Palidrome function that ignores white space & case senestive
# if a palidrome, will add it to the dictionary

def Palidromes(str1):
        size = str1.replace(" ", "")
        size = size.islower()
        length = reverse(str1)
        length = length.replace(" ", "")
        length = length.islower()
        if size == length:
                dict(str1)

# Main function for user input, displays results when user submits done

string = input("Enter the strings: ")

while string != "done" :
        Palidromes(string)
        string = input("Enter the strings: ")
else:
        print ("The Palindromes are: \n")
        print (list)
