##########################################################################
# Copyright (c) 2012, Benjamin Le Cam, Function Drawer <b.lecam@gmail.com>
#
# St. Olaf, Computer Science 125
# Fall 2012, Pr. Brown
#
# mainwindow.py
#
# This file describes the widget to draw a graph
#
##########################################################################

from graphics import *
from function import Function
from priceless import *
import math
from collections import namedtuple
from copy import copy
from threading import Thread, Lock

class UndrawerThread(Thread):
	def run(self, objects):
		for o in objects:
			o.undraw()

class DrawerThread(Thread):
	def run(self, obj, win):
		obj.draw(win)

class GraphWidget:
	def __init__(self, pt_left_bot, pt_right_top, win):
		self.function = Function("0")
		self.p1 = pt_left_bot
		self.p2 = pt_right_top
		self.graph_area = Rectangle(self.p1, self.p2)
		self.win = win
		self.accuracy = 0.1
		self.objects_drawn = []

	def getFunction(self):
		return self.func
	def setFunction(self, func):
		self.function = func

	def draw(self, xa, xb):
		self.cleanGraph()
		#Compute function and draw it
		x_min = min(xa, xb)
		x_max = max(xa, xb)
		
		#Compute all the values for f functon, accuracy give the step for computation
		fx = self.function.computeRange(x_min, x_max, self.accuracy)
		y_max = max(fx.values())
		y_min = min(fx.values())
		print(y_max, y_min)
		self.win.setCoords(x_min-(1/10)*x_max, y_min-(1/10)*y_max, x_max+(1/10)*x_max, y_max+(4/10)*y_max)

		x = x_min
		end = x_max
		prevfx = fx[x]
		k = 0
		while x < (end+self.accuracy):
			#p = Point(x, fx)
			#p.draw(mainwindow)
			u = fx[x]
			if k > 0:
				self.drawLine(x-self.accuracy, prevfx, x, u)
			prevfx = u
			x += self.accuracy
			k += 1

		self.drawAxis(x_min, x_max, y_min, y_max)
		


	def drawLine(self, x1, y1, x2, y2):
		l = Line(Point(x1, y1), Point(x2, y2))
		self.objects_drawn.append(l)
		drawer = DrawerThread()
		l.setOutline("blue")
		drawer.run(l, self.win)
		return

	def drawAxis(self, x_min, x_max, y_min, y_max):
		#Draw axes
		#draw x axs first
		#we first consider we will draw it where y=0
		x_axis = Line(Point(x_min, 0), Point(x_max, 0))
		if y_max < 0:
			#if all the x values are under 0
			#then we draw the on the top
			x_axis = Line(Point(x_min, y_max), Point(x_max, y_max))
		elif y_min > 0:
			#if all the x values are over 0
			#then we draw it at the bottom
			x_axis = Line(Point(x_min, y_min), Point(x_max, y_min))
		drawer = DrawerThread()
		drawer.run(x_axis, self.win)
		self.objects_drawn.append(x_axis)

		#we consider we will draw where x=0
		y_axis = Line(Point(0, y_min), Point(0, y_max))
		if x_max < 0:
			#if all the y values are under 0
			#then we draw the on right
			y_axis = Line(Point(x_max, y_min), Point(x_max, y_max))
		elif x_min > 0:
			#if all the y values are over 0
			#then we draw it at the bottom
			y_axis = Line(Point(x_min, y_min), Point(x_min, y_max))
		
		drawer = DrawerThread()
		drawer.run(y_axis, self.win)
		self.objects_drawn.append(y_axis)

		#draw x labels
		y_ax = x_axis.getP1().getY()
		x_step = x_max*(0.1)
		x_size = y_max*.01
		#from 0 to x_max
		x = 0
		togo = x_max+0.1
		while x < togo:
			sign = Line(Point(x, y_ax-x_size), Point(x, y_ax+x_size))
			drawer = DrawerThread()
			drawer.run(sign, self.win)
			self.objects_drawn.append(sign)
			if x != 0:
				text = str(int(x))
				if abs(x) < 1:
					text = ("{0:.1f}").format(x)
				label = Text(Point(x, y_ax-6*x_size), text)
				label.setSize(8)
				label.draw(self.win)
				self.objects_drawn.append(label)
			x += x_step
		#from 0 to x_min
		x = 0
		togo = x_min-(0.1)
		while x > togo:
			sign = Line(Point(x, y_ax-x_size), Point(x, y_ax+x_size))
			drawer = DrawerThread()
			drawer.run(sign, self.win)
			self.objects_drawn.append(sign)
			if x != 0:
				text = str(int(x))
				if abs(x) < 1:
					text = ("{0:.1f}").format(x)
				label = Text(Point(x, y_ax-6*x_size), text)
				label.setSize(8)
				label.draw(self.win)
				self.objects_drawn.append(label)
			x -= x_step
		#draw y labels
		x_ax = y_axis.getP1().getX()
		y_step = y_max*(0.1)
		y_size = x_max*(0.01)
		#from 0 to y_max
		y = 0
		togo = y_max+0.1
		while y < togo:
			print(y)
			sign = Line(Point(x_ax-y_size, y), Point(x_ax+y_size, y))
			drawer = DrawerThread()
			drawer.run(sign, self.win)
			self.objects_drawn.append(sign)
			if y != 0:
				text = str(int(y))
				if abs(y) < 1:
					text = ("{0:.1f}").format(y)
					y = float(text)
				label = Text(Point(x_ax-6*y_size, y), text)
				label.setSize(8)
				label.draw(self.win)
				self.objects_drawn.append(label)
			y = y+y_step
		#from 0 to y_min
		y = 0
		print(y_max, y)
		togo = y_min-0.1
		while y > togo:
			sign = Line(Point(x_ax-y_size, y), Point(x_ax+y_size, y))
			drawer = DrawerThread()
			drawer.run(sign, self.win)
			self.objects_drawn.append(sign)
			if y != 0:
				text = str(int(y))
				if abs(y) < 1:
					text = ("{0:.1f}").format(y)
					y = float(text)
				label = Text(Point(x_ax-6*y_size, y), text)
				label.setSize(8)
				label.draw(self.win)
				self.objects_drawn.append(label)
			y = y-y_step

	def cleanGraph(self):
		undrawer = UndrawerThread()
		undrawer.run(self.objects_drawn)
		self.objects_drawn = []

	def drawWuLine(self, x1, y1, x2, y2):
		xd = x2-x1
		yd = y2-y1
		if xd == 0 or yd == 0:
			print("Normal line")
			self.drawLine(x1, y1, x2, y2)

		else:
			if abs(xd) > abs(yd):
				#this is a vertical line
				#so we switch x and y

				if x1 < x2: #algorithm works only from min to max
					swap(x1, x2)
					swap(y1, y2)
		
				grad = yd/xd

				#first end point
				xend = round(x1)
				yend = y1+grad+(xend-x1)
				xgap = rfpart(x1+0.5)
				ix1 = round(xend)
				iy1 = int(yend)
				self.drawPixel(ix1, iy1, rfpart(yend)*xgap)
				self.drawPixel(ix1, iy1+1, fpart(yend)*xgap)
				yf = yend+grad

				#second end point
				xend = round(x2)
				yend = y2+grad*(xend-x2)
				xgap = fpart(x2+0.5)
				ix2 = round(xend)
				iy2 = int(yend)
				self.drawPixel(ix2, iy2, rfpart(yend)*xgap)
				self.drawPixel(ix2, iy2+1, fpart(yend)*xgap)

				#main loop
				x = ix1+1
				while x<(ix2-1):
					self.drawPixel(x, int(yf), rfpart(yf))
					self.drawPixel(x, int(yf)+1, fpart(yf))
					yf += grad
					x += 1
			elif abs(xd) < abs(yd):
				#this is a vertical line
				#so we switch x and y

				if y1 < y2: #algorithm works only from min to max
					swap(x1, x2)
					swap(y1, y2)
		
				grad = xd/yd

				#first end point
				yend = round(y1)
				xend = x1+grad+(yend-y1)
				ygap = rfpart(y1+0.5)
				iy1 = round(yend)
				ix1 = int(xend)
				self.drawPixel(ix1, iy1, rfpart(yend)*ygap)
				self.drawPixel(ix1, iy1+1, fpart(yend)*ygap)
				xf = xend+grad

				#second end point
				yend = round(y2)
				xend = x2+grad*(yend-y2)
				ygap = fpart(y2+0.5)
				iy2 = round(yend)
				ix2 = int(xend)
				self.drawPixel(ix2, iy2, rfpart(xend)*ygap)
				self.drawPixel(ix2, iy2+1, fpart(xend)*ygap)

				#main loop
				y = iy1+1
				while y<(iy2-1):
					self.drawPixel(int(xf), y, rfpart(xf))
					self.drawPixel(int(xf)+1, y, fpart(xf))
					xf += grad
					y += 1			

	def drawPixel(self, x, y, c):
   		p = Point(x, y)
   		#we convert the transparence c(0 to 1) to a rgb value(0 to 255)
   		c = math.floor(255*(1-c))
   		p.draw(self.win)



