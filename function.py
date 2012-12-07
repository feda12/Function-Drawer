##########################################################################
#Copyright (c) 2012, Benjamin Le Cam, Function Drawer <b.lecam@gmail.com>
#
#St. Olaf, Computer Science 125
#Fall 2012, Pr. Brown
#
#function.py
#
#This file describes a Function class
#
##########################################################################

import string
import copy
from collections import deque

from expression import Expression
from maths import Maths

#represents a mathematical function that can be drawn
class Function:

	def __init__(self, func_string, debug = False):
		self.original_string = func_string.strip()
		self.split_function = []
		self.rpn = []
		self.debug_state = debug
		if self.original_string != "":
			self.analyze()
		
	#split the function and create the rpn version
	def analyze(self):
		#function to split the original string function, and convert it to rpn
		#if the original string is empty, we do not need to go further
		if self.original_string == "":
			return

		self.split()
		self.generateRPN()

	#split the function into elements respecting mathematical functions operators and numbers
	def split(self):
		#Code to split a function into a list of numbers and expressions
		self.split_function = []
		split = [] #a temporary list with a shorter name to make the code clearer
		buffer_prev = ""
		func = self.original_string
		self.debug(("Function to be split is {0}").format(func))
		for f in func:
			#Creating the conditionnal tests variable for more clarity in the algorithm
			#Brackets are optionnal but makes it clearer
			prevEmpty = (buffer_prev == "")
			num = f.isdigit()
			prevnum = buffer_prev.isdigit()
			prevmathfunc = (buffer_prev in Maths.Expressions)
			operator = (f in Maths.Expressions)
			bracket = (f == "(" or f == ")")
			x = (f == "x")
			ascii = ord(f) #ascii value of f
			letter = (ascii >= 65 and ascii <= 90) or (ascii >= 97 and ascii <= 122)
			last_item = (f == func[len(func)-1])
			#a letter has an ascii value between 65 and 90 (caps), and between 97 and 122(non caps)

			#if it's a number, we chech the previous string
			# if previous string is empty or is a number, we add our number to the string  
			# if previous string is a mathematical operator, we add the latter to the elements and start a new string with our number
			if num:
				if prevEmpty or prevnum:
					buffer_prev += f
				elif prevmathfunc:
					split.append(buffer_prev)
					buffer_prev = f
				if last_item:
					split.append(f)

			#if it's a mathematical operator or a bracket
			# if previous string was a mathematical operator or a number, we add it to the list and clear previous string
			#we add the element to the list anyway
			elif operator or bracket:
				if prevmathfunc or prevnum:
					split.append(buffer_prev)
					buffer_prev = ""	
				split.append(f)


			#if that's a letter different from "x"
			# if previous string was a mathematical operator or a number, we add it to the list and change previous string to be equal to our new value
			# else we add our letter to the other letters
			elif letter and x == False:
				if prevmathfunc or prevnum:
					split.append(buffer_prev)
					buffer_prev = f
				else:
					buffer_prev += f
			
			#if we get x variable
			#if there is an e before(it would mean that the user typed exp), we add it to the string
			#elif, we chech if the previous string is a operator or a number, if it is, we add it to the list and clear the previous string
			#else it is a variable and we can just add it to our list
			elif x:
				if buffer_prev == "e": #case of exp(x)
					buffer_prev += f
				elif prevmathfunc or prevnum:
					split.append(buffer_prev)
					buffer_prev = ""
					split.append(f)
				else:
					split.append(f)

		self.split_function = copy.copy(split)
		self.debug(("Splitted function is {0}").format(self.split_function))
		return self.split_function

	#convert operators to Expression objects, and rearrange split list to match the rpn grammar
	def generateRPN(self): 
		#we initialize our rpn class variable to empty
		self.rpn = []

		#we create a deque object, it allows us to respect the principle of piles: last object added is on the top
		waitlist = deque()
		
		if self.debug:
			print(("\nGenerating Reverse Polish Notation for f(x)={0}\n").format(self.original_string))

		#we go for all the elements of the function
		for k in self.split_function:
			self.debug("-------------------------")
			#if k is a number, we add it to self.rpn
			if k.isdigit():
				self.debug(("{0} is a number").format(k))
				self.rpn.append(k)
			#we will consider x as a normal number in the conversion, however we will add brackets around it so our program
			#does not confuse with the 'x' of exp
			elif k == "x":
				self.rpn.append("[x]")
				self.debug(("{0} is a variable").format(k))
			#if k is an opening bracket, we add it to the pile so we could retrieve the priority order
			elif k == "(":
				self.debug(("Waitlist is {0}".format(waitlist)))
				waitlist.append(k)
				self.debug(("{0} is an opening bracket ").format(k))
				self.debug(("Now waitlist is {0}").format(waitlist))


			#if the string is an operator
			elif k in Maths.Expressions:
				#we create a duplicate of the expression to be able to add it in the rpn out list
				self.debug(("Waitlist is {0}".format(waitlist)))
				dup_expression = copy.deepcopy(Maths.Expressions[k])
				if self.debug:
					self.debug(("{0} is a math expression").format(k))
				#we get the size of the pile
				size_wait = len(waitlist)
				#if the list is not empty, we get the last item added without removing it
				if size_wait > 0:
					last_item = waitlist[size_wait-1]
				#if the pile is emp7
				if len(waitlist) == 0:
					self.debug("Waitlist is empty")
					waitlist.append(dup_expression)
				#elif the last item in the pile is an opening bracket, we add the operator to the pile
				elif last_item == "(":
					self.debug("Last item is a opening bracket")
					waitlist.append(dup_expression)
				#elif the priority of the operator is higher than the last item, we add the operator to the pile
				elif last_item != "(" and last_item != ")" and dup_expression.getPriority() < last_item.getPriority():
					self.debug("Last item is not a string and priority is higer")
					waitlist.append(dup_expression)
				#else, we remove the last item from the pile and add it to self.rpn
				else:
					self.debug("Else, we add a removed and add k")
					self.rpn.append(waitlist.pop())
					waitlist.append(dup_expression)
				self.debug(("Now waitlist is {0}").format(waitlist))

			#if we face a closing bracket, we remove all the operators from the pile and add them to self.rpn 
			#until we get an opening bracket, latter we delete
			elif k == ")":
				self.debug(("Waitlist is {0}").format(waitlist))
				self.debug(("{0} is a closing bracket ").format(k))
				u = ""
				while u != "(":
					u = waitlist.pop()
					if u != "(":
						self.rpn.append(u)
				self.debug(("Now waitlist is {0}").format(waitlist))
		
		#if there is any operators left in the pile, we add it to self.rpn
		#(verification of brackets is optionnal but in case)
		for i in range(len(waitlist)):
			u = waitlist.pop()
			if u != "(" and u != ")":
				self.rpn.append(u)

		self.debug(("\nReverse Polish Notation done.\n {0}\n").format(self.rpn))
		return self.rpn
		
	#compute the function, if there is no x in the function, it will make a simple calculation
	def compute(self, x_value = 0.0):
		results = []
		
		self.debug(("\nComputing f({0})").format(x_value))
		#we create a copy of the rpn version in order to plug x in it.
		tmp_rpn = copy.copy(self.rpn)

		x_count = tmp_rpn.count("[x]")
		#we make sure there is a variable before we call index function that would produce an error
		while x_count > 0:
			self.debug(("Occurences of x:{0}, x has to be {1}").format(str(x_count), str(x_value)))
			#we plug x value into the formula
			tmp_rpn[tmp_rpn.index("[x]")] = str(x_value)
			x_count -= 1
		
		#create a random expression object to compare the object type
		u = Expression("+", Maths.addition, 3, "addition")
		u_type = type(u)
		self.debug(("New RPN function is {0}").format(tmp_rpn))

		#we go through all the elements
		for t in tmp_rpn:
			t_type = type(t)
			#if this is a referenced expression, we call its compute function with the table as a function parameter 
			#this is part of the RPN grammar, there is always two numbers before an operator
			if t_type == u_type:
				self.debug(t.getAbbreviation())
				self.debug(results)
				t.compute(results)
			
			#else t is number, so we don't know what to compute: 
			#we convert it to a number and we add it to the results table
			elif type(t) == str and t.isdigit():
				results.append(eval(t))
			#in other case, the function don't know what do to with the element
			else:
				self.debug(("Hey I don't know what I should with that: {0} (index={1})").format(t, tmp_rpn.index(t)) )
		#the final result will be stocked in the first index of the table as it will be the only number left
		#but we still make sure there is at least one value otherwise we would get a memory location error
		if(len(results) == 0):
			return 0

		self.debug(("Computing done. f({0})={1}\n").format(x_value, results[0]))
		
		return results[0]

	#compute function from x=a to x=b and return a dictionnary
	def computeRange(self, a, b):
		values = {}
		#range to  b+1 because of python language
		for x in range(a, b+1):
			values[x] = self.compute(x)
		return values

	#return the string function entered by the user previously
	def getOriginal(self):
		return self.original_string

	#return the list of all the elements of function
	def getSplitFunction(self):
		return self.split_function

	#return the rpn notation of the function, using list
	def getRpn(self):
		return self.rpn
	
	#return the rpn notation of the function, using string
	def getRpnString(self):
		rpn_string = ""
		u = Expression("+", Maths.addition, 3, "addition")
		for k in self.rpn:
			if str(k).isdigit():
				rpn_string += str(k)
			elif type(k) == type(u):
				rpn_string += k.getAbbreviation()
			else:
				rpn_string += str(k)
			rpn_string += " "
		return rpn_string

	#change the debug state
	# true: message appears
	# false: nothing prints
	def setDebug(self, set = True):
		self.debug_state = set

	#return the debug state
	# true: message appears
	# false: nothing prints
	def getDebugState(self):
		return self.debug_state

	#print the object provided if debug state is true
	def debug(self, debug):
		if self.debug_state:
			print(debug)
