#Python Program to implement reverse and add function 

# Iterative function to reverse digits of num 
def reversDigits(num): 
	rev_num=0
	while (num > 0): 
		rev_num = rev_num*10 + num%10
		num = num/10
	return rev_num 

# Function to check whether the number is palindrome or not 
def isPalindrome(num): 
	return (reversDigits(num) == num) 

# Reverse and Add Function 
def ReverseandAdd(num): 
	rev_num = 0
	while (num <= 4294967295):
            num = num + rev_num
            if(isPalindrome(num)):
                print(num)
                break
            else:
                if (num > 4294967295):
                    print("No palindrome exist")

# Driver Code 
ReverseandAdd(363) 
ReverseandAdd(162) 
