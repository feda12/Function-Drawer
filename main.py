##########################################################################
#Copyright (c) 2012, Benjamin Le Cam, Function Drawer <b.lecam@gmail.com>
#
#St. Olaf, Computer Science 125
#Fall 2012, Pr. Brown
#
#mathematicalfunction.py
#
#This file is the main
#
##########################################################################

from function import Function
from maths import Maths
from mainwindow import MainWindow
from graphics import Point
import math

def main():
	Maths.generateMathExpressions()
	print("Available operators:")
	for o in Maths.Expressions:
		print(Maths.Expressions[o].getAbbreviation())

	print("-------------------------")
	f = Function("cos(3*x)+6/4*(x+3)", False)
	print("RPN String", f.getRpnString())
	for x in range (2, 11):
		f.compute(x)

	print("-------------------------")

	f = Function("56*((6+2)/(8-x)*2^3", False)
	print("RPN String", f.getRpnString()) #should give 56 6 2 + 8 7 - / 2 3 ^ * *


	mainwindow = MainWindow("Function Drawer", 992, 512)
	fx = f.computeRange(0, 10)
	max_y = max(fx.values())
	min_y = min(fx.values())

	print(min_y, max_y)
	mainwindow.setCoords(-1, min_y, 11, max_y)
	for x in range(0, 11):
		print(fx[x])
		p = Point(x, fx[x])
		p.draw(mainwindow)

	input("Press a key to quit")

main()