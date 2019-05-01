lis = [] # array list

# Main menu for user display
def Menu():
    print("A. See the list ")
    print("B. Add to the list ")
    print("C. Subtract from the list")
    print("D. Delete the entire list")
    print("E. See the size of your list")
    print("F. Reverse")
    print("G. Search the list")
    print("H. Quit")

# Switch statement for user option
def Switch(option):
    option = option.upper()
    switch = {
        "A": PrintList,
        "B": Insert,
        "C": Delete,
        "D": StartOver,
        "E": Size,
        "F": Reverse,
        "G": Search,
    }
    return switch.get(option, "Wrong choice")()

# Prints the array
def PrintList():
    print(lis)

# Inserts a certain value at a certain index
def Insert():
    index = input("Enter the index of the array: ")
    index = int(index)
    phrase = input("Enter a word: ")
    lis.insert(index, phrase)
    print(lis)

# Deletes a certain value at a certain index
def Delete():
    deletion = input("Enter an index of the array: ")
    deletion = int(deletion)
    lis.pop(deletion)
    print(lis)

# Deletes the entire array
def StartOver():
    del lis[0 : len(lis)]

# Prints the size of the array
def Size():
    print(len(lis))

# Reverses the array
def Reverse():
    print(list(reversed(lis)))

# Searches a certain value in the array
def Search():
    seek = input("Enter a string to search: ")
    counter = 0
    for x in range(0, answer):
        if (lis[x] == seek):
            counter+= 1
    print("There is", counter, seek, "in the list ")

# main function
if __name__ == "__main__":
    answer = input("Enter a size for your array: ")
    answer = int(answer)
    if (answer < 1):
        print("This is not a value size. Please try again later..")
    else:
        i = 0
        while (i < answer):
            sentence = input("Enter a string: ")
            lis.append(sentence)
            i+=1
    Menu()
    choice = input("Enter a choice: ")
    while (choice != 'H' and choice != 'h'):
        Switch(choice)
        Menu()
        choice = input("Enter a choice: ")
    print("Goodbye")
    
