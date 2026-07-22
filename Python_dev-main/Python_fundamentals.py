'''

name = "Sai"
age = 25
gender = "Male"
salary = 1000000.00

print("Name:",name)
print("Gender:",gender)

Data types in Python:
1. Numeric types: int, float, complex
2. Sequence types: list, tuple, range
3. Text type: str

name = "Chandan"         # "String"
age = 25                # "Integer"
height = 6.1            # "Float"
is_developer = True      # "Boolean"

#Check type of variable
print(type(name))        # <class 'str'>
print(type(age))     # <class 'int'>
print(type(height))  # <class 'float'>

name = input("Enter your name: ")   #Input function to take user input (name)
age = input("Age:")                 #Input function to take user input (age)

print("Name:", name)                #output the name entered by user
print("Age:", age)                  #output the age entered by user

name = input("Enter your name: ")   #Input function to take user input (name)

print("Welcome", name)

Arithmetic operations in Python:
1. Addition: +
2. Subtraction: -
3. Multiplication: *
4. Division: /
5. Modulus: %


# Let us suppose we have two numbers, a = 10 and b = 3. We can perform arithmetic operations on these numbers as follows:

a=10
b=3

print("Addition:", a + b)          # Output: 13
print("Subtraction:", a - b)       # Output: 7
print("Multiplication:", a * b)    # Output: 30
print("Division:", a / b)          # Output: 3.3333333333333335
print("Modulus:", a % b)            # Output: 1
print("Exponentiation:", b ** a)    # Output: 59049

#Comparison operators in Python:
print("Comparison Operators:")
print(a == b)       #False 
print(a < b)        #False
print(a > b)        #True
print(a <= b)       #False
print(a >= b)       #True
print("\n")
#Logical loperators in Python:
print(a>2 and a!=5)  #True



#if conditional statements in Python:
Age = input("Enter your age: ")

if(Age >= 18):
    print("You are eligible to vote.")


Age = input("Enter your age:")

if int(Age) >= 18:
    print("Adult")
else:
    print("Not Adult")

    

#if-elif-else conditional statements in Python:

Marks = int(input("Enter marks:"))          #input function to take user input (marks)
if(Marks >= 90):                            #if condition to check if marks are greater than or equal to 90
    print("Grade A+")                       #print statement to output grade A+ if condition is true
elif(Marks < 90 and Marks >= 80):           #elif condition to check if marks are less than 90 and greater than or equal to 80
    print("Grade A")                        #print statement to output grade A if condition is true
elif(Marks < 80 and Marks >= 70):           #elif condition to check if marks are less than 80 and greater than or equal to 70
    print("Grade B")                        #print statement to output grade B if condition is true
else:                                       #else condition to check if none of the above conditions are true
    print("Grade C")                        #print statement to output grade C if none of the above conditions are true
    

#for loop in Python:

for i in range(1, 11):                  #for loop to iterate through numbers from 1 to 10
    print(i)                    
    


#while loop in Python:

Count = 1                       #Initialize Count variable to 1
while Count <= 10:              #while loop to iterate through numbers from 1 to 10
    print(Count)                #Printing the value of Count in each iteration of the loop
    Count += 3                  #Incrementing the value of Count by 3 in each iteration of the loop
    


#Functions in Python(with parameters):

def greet(name):                     #Defining a function named greet that takes a parameter name
    print("Hello, " + name + "!")    #Printing a greeting message with the name passed as an argument
    
    
greet("SAI")                               #Calling the greet function with the argument "SAI" 




def greet():                                #defining a function named greet that takes no parameters
    print("Hello python!")
    
greet()



#return statement in Python:


def add(a,b):
    return a + b

result = add(5, 3)

print("The sum is:", result)

'''


