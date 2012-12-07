##########################################################################
# Copyright (c) 2012, Benjamin Le Cam, Function Drawer <b.lecam@gmail.com>
#
# St. Olaf, Computer Science 125
# Fall 2012, Pr. Brown
#
# expression.py
#
# This file describes a Mathematical function expression
#
##########################################################################

import string

#represents a mathematical element from a function(not a number).
class Expression:
	def __init__(self, abbreviation, compute_function, priority, name = "", category = "Other"):
		self.name = name
		self.abbreviation = abbreviation
		self.priority = priority
		self.compute_function = compute_function
		self.category = category


	def setName(self, name):
		self.name = name
	def setAbbreviation(self, abbreviation):
		self.abbreviation = abbreviation
	def setPriority(self, priority):
		self.priority = priority
	def setComputeFunction(self, compute_function):
		self.compute_function = compute_function
	def setCategory(self, category):
		self.category = category

	def getName(self): 
		return self.name
	def getAbbreviation(self):
		return self.abbreviation
	def getPriority(self):
		return self.priority
	def getCategory(self):
		return self.category
	#call to the function defined by expression
	#no need to check validity as it is mandatory in the constructor
	def compute(self, results_stack):
		return self.compute_function(results_stack)



