##########################################################################
# Copyright (c) 2012, Benjamin Le Cam, Function Drawer <b.lecam@gmail.com>
#
# St. Olaf, Computer Science 125
# Fall 2012, Pr. Brown
#
# math.py
#
# This file describes a Math class. Math class is used to represents all the
# mathematical functions used by the program and also contains a dictionnary
# of all this functions
#
##########################################################################

from expression import Expression
import math

#class representing the math functions and a dictionnary of all of them
class Maths:
	Expressions = {}

	#creating all the mathematical operations object and adding them to the dictionnary, index is abbreviation of the function
	@staticmethod
	def generateMathExpressions():
		expressions = []
		expressions.append(Expression("+", Maths.addition, 3, "addition"))
		expressions.append(Expression("-", Maths.substraction, 3, "substraction"))
		expressions.append(Expression("*", Maths.multiplication, 2, "multiplication"))
		expressions.append(Expression("/", Maths.division, 2, "division"))
		expressions.append(Expression("^", Maths.pow, 1, "power"))
		expressions.append(Expression("%", Maths.remainder, 3, "remainder"))
		expressions.append(Expression("abs", Maths.abs, 0, "absolute value"))
		expressions.append(Expression("cos", Maths.cos, 0, "cosinus"))
#		expressions.append(Expression("sin", Maths.sin, 0, "sinus"))
#		expressions.append(Expression("tan", Maths.tan, 0, "tangent"))
#		expressions.append(Expression("arccos", Maths.arccos, 3, "arc cosinus"))
#		expressions.append(Expression("arcsin", Maths.arcsin, 3, "arc sinus"))
#		expressions.append(Expression("arctan", Maths.arctan, 3, "arc tangent"))
#		expressions.append(Expression("pi", Maths.pi, 0, "pi"))
#		expressions.append(Expression("exp", Maths.exp, 0, "exponential"))
#		expressions.append(Expression("ln", Maths.ln, 0, "logarithm neperian"))
#		expressions.append(Expression("log", Maths.exp, 0, "logarithme"))
#		expressions.append(Expression("sqrt", Maths.log, 0, "square root"))
#		expressions.append(Expression("exp", Maths.exp, 0, "exponential"))
#		expressions.append(Expression("!", Maths.exp, 0, "factorial"))

		#Then we add them to the dictionnary using their abbreviations as key because user will use abbreviations in the formula
		for o in expressions:
			Maths.Expressions[o.getAbbreviation()] = o

	#Modified versions of built-in operations and math operations
	@staticmethod
	def addition(rpn_stack):
		a = rpn_stack.pop()
		b = rpn_stack.pop()
		rpn_stack.append(a+b)
	
	@staticmethod
	def substraction(rpn_stack):
		b = rpn_stack.pop()
		a = rpn_stack.pop()
		rpn_stack.append(a-b)

	@staticmethod
	def multiplication(rpn_stack):
		a = rpn_stack.pop()
		b = rpn_stack.pop()
		rpn_stack.append(a*b)

	@staticmethod
	def division(rpn_stack):
		b = rpn_stack.pop()
		a = rpn_stack.pop()
		if b == 0:
			rpn_stack.append(0)
			return
		rpn_stack.append(a/b)

	@staticmethod
	def pow(rpn_stack):
		b = rpn_stack.pop()
		a = rpn_stack.pop()
		rpn_stack.append(a**b)

	@staticmethod
	def remainder(rpn_stack):
		b = rpn_stack.pop()
		a = rpn_stack.pop()
		rpn_stack.append(a%b)

	@staticmethod
	def abs(rpn_stack):
		a = rpn_stack.pop()
		rpn_stack.append(abs(a))

	@staticmethod
	def exp(rpn_stack):
		a = rpn_stack.pop()
		rpn_stack.append(math.exp(a))

	@staticmethod
	def cos(rpn_stack):
		a = rpn_stack.pop()
		rpn_stack.append(math.cos(a))




