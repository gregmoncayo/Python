import base64
import random 
import time 
import datetime
from tkinter import *

Dict = {}
Pass = {}

class Account():
    def __init__(self, description):
        self.description = description

    def Add(name, password):
        Dict.__setitem__(0, name)
        Pass.__setitem__(0, Account.encryption("12", password))

    def encryption(key, clear):
        encode = []

        for x in range(len(clear)):
            key2 = key[x % len(key)]
            enc = chr((ord(clear[x]) + ord(key2)) % 256)

            encode.append(enc)

        return base64.urlsafe_b64encode("".join(encode).encode()).decode()

    def decode(key, encod):
        dec = []

        encod = base64.urlsafe_b64decode(encod).decode()

        for x in range(len(encod)):
            primekey = key[x % len(key)]
            secondary = chr((256 + ord(encod[i]) - ord(primekey)) % 256)

            secondary.append(secondary)

        return "".join(secondary)

    def Menu():
        print("1. Add Account ")
        print("2. Delete Account ")
        print("3. Show accounts ")
        print("4. Check if passwords match ")
        print("5. Exit ")

    def DoMenu(choice = None):
        if (choice == 1):
            name = input("Enter a username: ")
            password = input("Enter a password: ")
            Account.Add(name, password)
        if (choice == 2):
            Account.DeleteAccount()
        if (choice == 3):
            print(Dict)
        if (choice == 4):
            Account.Check()

    def DeleteAccount():
        name = input("Enter username: ")

        for key, value in list(Dict.items()):
            if (value == name):
                del Dict[key]

    def Check():
        n = input("Enter the username: ")
        p = input("Enter the password: ")
        flag = False
        Flag1 = False

        for key, value in Dict.items():
            if (value == n):
                flag = True
                
        for key, value in Pass.items():
            if (value == Account.encryption("12", p)):
                Flag1 = True

        if (flag == True):
            print ("Username matches with our system. ")
        else:
            print("Username does not match within our system. ")

        if (Flag1 == True):
            print("Password matches with our system. ")
        else:
            print("Password does not match within our system. ")
    
if __name__ == "__main__":
    A = Account.Menu()
    g = input("> ")
    g = int(g)
    while (g != 5):
        A = Account.DoMenu(g)
        A = Account.Menu()
        g = input("> ")
        g = int(g)
