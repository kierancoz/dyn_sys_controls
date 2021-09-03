#--------------------------------------------------------------------------
# File for basic python use
# ME 144L - Fall 2020
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# Begin by importing packages and renaming them (for brevity)
# import [package name] as [new call name]
#--------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
from sklearn.linear_model import LinearRegression 

#--------------------------------------------------------------------------
# Variables and Print Commands
#--------------------------------------------------------------------------
# quintessential beginning statement when learning code
# print("Hello World") 

# # Types of variables
# string = "string of characters "
# number = 1.5
# List   = [1,2,3,4,5]
# Tuple  = ("String", number, List) # A tuple can group various types of data together

# # Use print() command to output variables to the Console
# print(string)
# print(number)
# print(List, Tuple) # Can print more than one at a time

# # Can add strings and functions/math in the print command
# print("String Variable*2 =", string*2)  # Can also multiply strings
# print("Number/2 =", number/2)

# # Can convert numbers into different formats 
# print("int(number) =", int(number))     # Note: int() truncates; does not round
# print("round(number) =", round(number)) # Use round() function to round numbers
# print("\n")                             # Prints a new line


# #--------------------------------------------------------------------------
# # Math commands, arrays, lists
# #--------------------------------------------------------------------------
# a,b = 5,2

# add = a + b
# sub = a - b
# mult,div = a*b, a/b
# exponent = a**b

# # Output the values to the console
# print("a =", a, ", b =", b)
# print("a+b =", add, ", a-b =", sub)
# print("a*b =", mult, ", a/b =", div, ", a^b =", exponent)
# print("\n")

# # Create a numerical array using np.linspace or np.arange function
# X = np.linspace(0,5,11) # creates an array from 0 to 5 with 11 equally spaced values (includes both 0 and 5)
# Y = np.arange(10,21,1)  # creates an array from 10 to 20 with increments of 1 (does not include 21, stops at 20)

# # Turn a numerical array into a list
# Xl = list(X)
# Yl = list(Y)

# print("X= ",X)
# print("Y= ",Y)
# print("\n") 



# #--------------------------------------------------------------------------
# # Loops
# #--------------------------------------------------------------------------
# # For loops require the number of iterations to run
# # Use range() command to dictate iteration count

# its = 5                    # number of iterations we want the For Loop to run
# loop_var = []              # creates an empty list to be filled in the For Loop
# for i in range(its):       # For loop will run 'its' times (its = 5)
#     value = List[i]        # uses the iteration variable 'i'
#     loop_var.append(value) # adds 'value' to the loop_var variable

# print("For loop output =", loop_var)
    

# # While Loops run until a condition to exit is met

# j = 0 # beginning While Loop counter
# while_var = []
# while (j < 10):         # The loop ends when j = 10
#     j = j+1             # Make sure to update j each iteration otherwise loop will run forever
#     while_var.append(j) # adds 'j' to the while_var list

# print("While loop output =", while_var)
# print("\n")



#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
# Student Exercise #1: 
#
#     1) Make a list, List1, from 0 to 10
#         --> Include both 0 and 10 in the list
#         --> Use increments of 2
#     2) Square each component of the array using the For Loop below and print
#
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

List1 = list(range(0,11))
Squares = [i**2 for i in List1]
print("Squares =", Squares)
print("\n")





#--------------------------------------------------------------------------
# Comparison Operators, If/Else statements
#--------------------------------------------------------------------------
# set x and y as any numeric values 
# x,y = 10,20

# # If, Else If (elif), and Else statements
# # Note: Loops can be nested
# if (x>y):
#     print("x is the largest")
# elif (x<y):
#     print("y is the largest")
# else:
#     print("x is equal to y")
# print("\n")


#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
# Student Exercise #2: 
#
# Using the If/Else statment structure provided below, write a code that:
#     1) Compares the variables z1 and z2
#     2) If z2 is larger --> solve and print z3 = z1*z2 
#     3) If z1 is larger --> solve and print z3 = z1/z2 
#
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

#z1,z2 =
# if():
#
# else:
#



#--------------------------------------------------------------------------
# # Write a text/CSV file
# #--------------------------------------------------------------------------
# # Method 1: Use csv writer package
# with open("temp.csv","w",newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows([X,Y])


        
# # Method 2: Using pandas
# filename  = 'calibrationDataWithPandas.csv'
# data_dict = {'x_data': X, 'y_data': Y} # Create a dictionary with your desired column names and data
# data_df   = pd.DataFrame(data_dict)    # Convert dicitonary into dataframe
# data_df.to_csv(filename,index=False)   # Write data to csv without indices




# # Method 1: CSV package

# # Can pull directly from csvdata using indices: csvdata[0,1]
# csvread = np.loadtxt('temp.csv',delimiter=',')
# print("csv data =",csvread, "\n")

# # Separate variables and manipulate data
# Xc1 = csvread[0,:]
# Yc1 = csvread[1,:]/2 - 5 # Can manipulate data when indexing


# # Method 2: pandas package
# csvdata = pd.read_csv('calibrationDataWithPandas.csv')

# # index into the columns using the column header names
# Xc2 = csvdata.x_data
# Yc2 = csvdata.y_data/2 # Can manipulate data when indexing

# print("Xc2 = ", Xc2, "\n")
# print("Yc2 = ", Yc2, "\n")

# # Plot the XY data using a scatter plot
# plt.figure(1)
# plt.scatter(Xc1, Yc1)
# plt.scatter(Xc2, Yc2)
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.legend(['Y/2 - 5', 'Y/2'])
# plt.title('Y versus X')
# plt.grid()
# plt.show()




# #--------------------------------------------------------------------------
# #--------------------------------------------------------------------------
# # Student Exercise #3: 
# #
# # Using the variables Xdata and Ydata
# #     1) Save the variables to a CSV file using the pandas method (method 2)
# #     2) Read the file and assign the data to new variables (Xd1, Yd1)
# #     3) Plot Yd1 versus Xd1 in a scatter plot with labeled axes and a title
# #
# #--------------------------------------------------------------------------
# #--------------------------------------------------------------------------

# Xdata = np.linspace(0,10,101)
# Ydata = Xdata**3 - 8*Xdata**2 + 6*Xdata +10

# filename  = 'Exercise3.csv'
# # --------------------
# # Insert code here:




# # --------------------
# # Uncomment below when Xd1 and Yd1 have been populated
# # plt.figure(2)
# # plt.scatter(Xd1,Yd1)
# # plt.show()




# #--------------------------------------------------------------------------
# # Perform a Linear Regression (using sample Potentiometer data)
# #--------------------------------------------------------------------------
# # Calibration Values
# Ints   = np.array([148,482,831]).reshape((-1,1))
# Angles = np.linspace(-90,90,3)

# # Linear Regression
# model    = LinearRegression().fit(Ints, Angles.reshape(-1, 1))
# Rsquared = model.score(Ints, Angles)
# slope, intercept = model.coef_, model.intercept_
# print('intercept =', intercept)
# print('slope =', slope)
# print('coefficient of determination =', Rsquared)

# # Plot the raw data and regression using a scatter plot
# plt.figure(2)
# plt.scatter(Ints,Angles, c="r", marker='x')
# plt.plot(Ints,slope*Ints + intercept)
# plt.xlabel('Ints')
# plt.ylabel('Angles [deg]')
# plt.legend(['Lin. Reg.','Raw Data'])
# plt.title('Regression of Sensor Data')
# plt.grid()
# plt.show()














