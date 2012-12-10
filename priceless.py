##########################################################################
#Copyright (c) 2012, Benjamin Le Cam, Function Drawer <b.lecam@gmail.com>
#
#St. Olaf, Computer Science 125
#Fall 2012, Pr. Brown
#
#priceless.py
#
#This file include functions that are super useful
#
##########################################################################

#check if s(a string) is a number
#isdigit only check integers
def isNumber(s):
    try:
        float(s)
        return True
    except ValueError or TypeError:
        return False

#Ucheck if b is between a and b
def between(a, b, c):
	if a <= b <= c or c <= b <= a:
		return True
	return False

def swap(a, b):
	a, b = b, a

def fpart(a):
	return a-(int(a))

def rfpart(a):
	return 1-fpart(a)