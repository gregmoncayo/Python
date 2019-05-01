#!/usr/bin/env python

# Gregory Moncayo
# FSUID: glm16b
# 09/18/2018

# Binomial coefficient formula

def add(a,b):
    answer = 1
    if (b > a - b): 
        b = a - b
    for x in range(0 , b): 
        answer = answer * (a - x)
        answer = int(answer / (x + 1))

    return answer

'''    
 Two nested for loops to print the rows and columns
 prints spaces and end ="" to stop the string overflowing
 with spaces
 print() is to print a new line
'''

def printTriangle(n):
    for x in range(0,n):
        for y in range(0,x+1):
            sum = add(x,y)
            print(sum, " ", end = "")
        print()

# User input for main menu

number = input ("Enter the number of rows: ")
num = int(number)

''' If users inputs a number below 3,
    automatically prints a triangle of 3.
    If entered correctly, prints the user's
    triangle
'''

if (num < 3):
    printTriangle(3)
else:
    printTriangle(num)
