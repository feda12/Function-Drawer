##########################################################################
# Copyright (c) 2012, Benjamin Le Cam, Function Drawer <b.lecam@gmail.com>
#
# St. Olaf, Computer Science 125
# Fall 2012, Pr. Brown
#
# mainwindow.py
#
# This file describes the main window of Function Drawer
#
##########################################################################

from graphics import *
import string
from button import Button

class MainWindow(GraphWin):
	def __init__(self, title, width, height):
		super(MainWindow, self).__init__(title, width, height)
		self._width = width
		self.height = height
		self.setCoords(-30, self.height, self.width, -20)
		#setting up gui
		function_label = Text(Point(0, 0), "f(x)=")
		function_label.setSize(16)

		entry_width = int((width-100)/(function_label.getTextWidth()/len(function_label.getText())))
		print(entry_width)
		self.function_input = Entry(Point((width-20)/2, 0), entry_width)

		go_button = Button("Go", Point(width-35, -12), Point(width-2, 11))

		function_label.draw(self)
		self.function_input.draw(self)
		go_button.draw(self)

