import queue

class Queue:
    # Default Constructor
    def __init__(self):
        self.lis = []

    # Prints the Queue
    def SeeQueue(self):
        for x in range(0, len(lis)):
            print(lis[x])
            
    # Checks if the list is empty
    def IsEmpty(self):
        if (len(lis) == None):
            return True
        return False

    # Checks if the Queue is empty
    def Empty(self):
        return self.lis == []

    # Adds to the list
    def Enqueue(self, value):
        self.lis.insert(0, value)

    # Deletes from the list
    def Dequeue(self):
       return self.lis.pop()

    # Returns the size of the list
    def Size(self):
        return len(self.lis)

    def Search(self, value):
        for x in range(0, len(lis)):
            for y in range(0, x):
                if (lis[x] == lis[y]):
                    return True
        return False

    # Reverses the list
    def Reverse(self):
        print(list(reversed(lis)))

    # Main menu for user experience
    def MainMenu(self):
        print("A. See Queue")
        print("B. Check if Queue is empty")
        print("C. Add to the list")
        print("D. Delete from the list")
        print("E. Empty list")
        print("F. Reverse")
        print("G. Search")
        answer = input("Enter a choice: ")
        Queue.Switcher(answer)

    # Switch statement for user input
    def Switcher(self, choice):
        choice = option.upper()
        switch = {
        "A": SeeQueue,
        "B": IsEmpty,
        "C": Enqueue,
        "D": Dequeue,
        "E": Empty,
        "F": Reverse,
        "G": Search,
        }
        return switch.get(choice, "Wrong choice")()
    
# main function
if __name__ == "__main__":
    q=Queue()
    q.MainMenu()
    
    
