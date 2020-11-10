# test

import time
import board
import math
from adafruit_extended_bus import ExtendedI2C as I2C
import Adafruit_MCP4725
import RPi.GPIO as GPIO

import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import numpy as np


GPIO.setmode(GPIO.BCM)


dac1 = Adafruit_MCP4725.MCP4725(address=0x60)
dac2 = Adafruit_MCP4725.MCP4725(address=0x61)
(dacx,dacy)=(dac1,dac2)

im_file="out.svg"

interval=.1
maxr=4096

pen_interval=.5
move_interval=.05

pen_up_pin=4
GPIO.setup(pen_up_pin, GPIO.OUT)

def clamp(n):
	return min(max(n,0),1)

def pltmove(x,y):
	vx=int(clamp(x)*maxr)
	vy=int(clamp(y)*maxr)
	print("("+str(vx)+","+str(vy)+")")
	dacx.set_voltage(vx)
	dacy.set_voltage(vy)

def pltmove1(c):
	pltmove(c[0],c[1])

# might need to reverse these two depending
def pen_up():
	GPIO.output(pen_up_pin,GPIO.LOW)
	print("pen up")
	
def pen_down():
	GPIO.output(pen_up_pin,GPIO.HIGH)
	print("pen down")


def circle_test():
	while 1:
		for n in range(0,100):
			nx=(math.sin(n/100.0*math.pi*2)+1)/2
			ny=(math.cos(n/100.0*math.pi*2)+1)/2
			# ~ print("("+str(nx)+","+str(ny)+")")
			pltmove(nx,ny)
			time.sleep(interval)

def pen_updown_test():
	while 1:
		pen_up()
		time.sleep(1)
		pen_down()
		time.sleep(1)

def load_image(im):
	# load file from https://github.com/LingDong-/linedraw
	tree = ET.parse(im)
	lines=[]
	for child in tree.getroot():
		l=[float(x) for x in child.attrib["points"].split(",")]
		p=[[l[(2*n)],l[(2*n)+1]] for n in range(0,int(len(l)/2))]
		# ~ print(p)
		lines.append(p)
	return lines

def get_dimensions(lines):
	maxx=max([p[0] for l in lines for p in l])
	maxy=max([p[1] for l in lines for p in l])
	return (maxx,maxy)

def scale_point(p,dim):
	return [p[0]/dim[0],p[1]/dim[1]]

def draw_image(lines):
	dim=get_dimensions(lines)
	pen_up()
	for line in lines:
		pltmove1(scale_point(line[0],dim))
		time.sleep(pen_interval)
		pen_down()
		time.sleep(pen_interval)
		for point in line[1:]:
			pltmove1(scale_point(point,dim))
			time.sleep(move_interval)
		pen_up()
		time.sleep(pen_interval)

print(get_dimensions(load_image(im_file)))

try:
	# ~ circle_test()
	# ~ pen_updown_test()
	draw_image(load_image(im_file))
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup(pen_up_pin)
	print("done")

