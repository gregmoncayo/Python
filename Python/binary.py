
#
# Complete the 'decode' function below.
#
# The function is expected to return a STRING.
# The function accepts following parameters:
#  1. STRING_ARRAY codes
#  2. STRING encoded
#
s = ""
st = []
def decode(codes, encoded):
    # Write your code here
    global s
    d = str(encoded)

    d = list(d)
    z = ""
    global st
    for i in range(0, len(d)):
        z = z + d[i]
        if (i % 6 == 0):
            st.append(z)
            z = ""   
    for x in range(0, len(st)):
        if (st[x] == "100100"):
            s = s + "a"
        if (st[x] == "100101"):
            s = s + "b"
        if (st[x] == "110001"):
            s = s + "c"
        if (st[x] == "100000"):
            s = s + "d"
        if (st[x] == "111111"):
            s = s + "\n"
        if (st[x] == "111110"):
            s = s + "p"
        if(st[x] == "000001"):
            s = s + "q"
    return s

if __name__ == '__main__':
 #   fptr = open(os.environ['OUTPUT_PATH'], 'w')

    print("Enter a count: ")
    codes_count = int(input().strip())

    codes = []

    for _ in range(codes_count):
        codes_item = input()
        codes.append(codes_item)

    encoded = input()

    result = decode(codes, encoded)

    fptr.write(result + '\n')

    fptr.close()
