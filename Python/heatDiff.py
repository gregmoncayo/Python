#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
def calculate(s):
    t = np.arange(0., s+1, 1.)
    for x in range(0, s):
        plt.plot(t, t**0+x, 'ro')
        if (t[x-1] == 5):
            plt.plot(t,t**0+x, 'bo')
        if (t[x+1] == 6):
            plt.plot(t,t**0+x, 'yo')
        if (t[x] == 4):
            plt.plot(t, 'go')
    plt.axis([0, s, 0, s]) # x and y range of axis
    plt.show()

if __name__ == "__main__":
    answer = input("Please enter a temperature: ")
    answer = int(answer)
    calculate(answer)
