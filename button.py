##########################################################################
#Copyright (c) 2012, Benjamin Le Cam, Function Drawer <b.lecam@gmail.com>
#
#St. Olaf, Computer Science 125
#Fall 2012, Pr. Brown
#
#button.py
#
#This file describes a Button class
#
##########################################################################

from graphics import *
from priceless import *

class Button:
	def __init__(self, text, pt1, pt2): 
		self._pt1 = pt1
		self._pt2 = pt2
		self._rect = Rectangle(pt1, pt2)
		self._label = Text(self._rect.getCenter(), text)
	
	def getLabel(self):
		return self._label.getText()
	def getPt1(self):
		return self._pt1
	def getPt2(self):
		return self._pt2
	def getRect(self):
		return self._rect
	
	def setLabel(self, text):
		self._label.setText(text)
	def draw(self, window):
		self._rect.draw(window)
		self._label.draw(window)
	def inButton(self, pt):
		x1 = self._pt1.getX()
		y1 = self._pt1.getY()
		x2 = self._pt2.getX()
		y2 = self._pt2.getY()
		if between(x1, pt.getX(), x2) and between(y1, pt.getY(), y2):
			return True
		return False
	def move(self, x, y):
		self._pt1 = Point(self._pt1.getX()+x, self._pt1.getY()+y)
		self._pt2 = Point(self._pt2.getX()+x, self._pt2.getY()+y)
		self._rect = Rectangle(self._pt1, self._pt2)
		self._label = Text(self._rect.getCenter(), self._label.getText())
