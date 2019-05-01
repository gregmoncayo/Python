import collections

def breakUp(word):
    count = len(word.split())
    value = []
    letters = []
    counter = 0
    for x in range (0, count):
        statement = word.split()
        letter = [c for c in statement[x]]
        letterCounter = len(letter)
        for y in range(0, letterCounter):
            letters.append(letter[y])
            if (ord(letter[y]) > 64 and ord(letter[y]) < 123):
                value.append(ord(letter[y]))
    print("The numbers of letters within the sentence: ")
    for q in range(0, len(value)):
        for s in range(0, q):
            if (value[0] == value[q]):
                counter = counter + 1
        print(letters[q], "-", counter)
    
if __name__ == "__main__":
    sentence = input ("Enter a string: ")
    sentence = sentence.lower()
    breakUp(sentence)
