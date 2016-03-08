from sense_hat import SenseHat
from time import sleep
from random import randint
from evdev import InputDevice, list_devices, categorize, ecodes
import thread
import colorsys
import random

dev = InputDevice('/dev/input/event0')
sense = SenseHat()

currentMode = 0
totalModes = 3
lastRun = totalModes

modeNameScrollSpeed = .03

colorStep = .04

replies = ['Signs point to yes',
           'Without a doubt',
           'You may rely on it',
           'Do not count on it',
           'Looking good',
           'Cannot predict now',
           'It is decidedly so',
           'Outlook not so good'
           ]

def keyboard_listener(name, delay):
	global currentMode
	global totalModes
	global sense
	for event in dev.read_loop():
		if event.type == ecodes.EV_KEY:
			if (event.code == 28) and (event.value == 0):
				currentMode = 0
			if (event.code == ecodes.KEY_UP) and (event.value == 0):
				currentMode = 1
			if (event.code == ecodes.KEY_DOWN) and (event.value == 0):
				currentMode = 2
			if (event.code == ecodes.KEY_LEFT) and (event.value == 0):
				currentMode = 3
			if (event.code == ecodes.KEY_RIGHT) and (event.value == 0):
				currentMode = 4	

thread.start_new_thread(keyboard_listener, ("Thread-1", 2, ))

while True:
	if currentMode == 0:
		if lastRun is not currentMode:
			sense.set_rotation(0)
			hue = 0.0
			sense.clear()
			lastRun = currentMode
		for y in range(0,8):
			newColor = list(colorsys.hls_to_rgb(hue+(y*colorStep), .5, 1))
			newColor[0] = int(newColor[0] * 255)
			newColor[1] = int(newColor[1] * 255)
			newColor[2] = int(newColor[2] * 255)
			for x in range(0,8):
				sense.set_pixel(x,y,newColor)
		sleep(.03)
		hue = hue + colorStep
		if hue + colorStep > 1.0:
			hue = hue - 1.0
	if currentMode == 1:
		if lastRun is not currentMode:
			sense.set_rotation(0)
			lastRun = currentMode
		temp = sense.temp
		temp = temp*1.8 + 32
		humidity = sense.get_humidity()
		humidity_value = 64 * humidity / 100
		humidity_value = round(humidity_value,1)
		temp = round(temp, 1)
		sense.show_message("Temp: " + str(temp) + " Humidity: " + str(humidity_value) + "%", scroll_speed=.05)
		currentMode = 0
	if currentMode == 2:
		if lastRun is not currentMode:
			sense.load_image("/home/pi/maker-faire-sense-hat-demo/logo.png")
			lastRun = currentMode
		x, y, z = sense.get_accelerometer_raw().values()
		x = round(x, 0)
		y = round(y, 0)
		if x == -1:
			sense.set_rotation(180)
		elif y == 1:
			sense.set_rotation(270)
		elif y == -1:
			sense.set_rotation(90)
		else:
			sense.set_rotation(0)

	if currentMode == 3:
		if lastRun is not currentMode:
			# first execution stuff here if needed
			sense.set_rotation(0)
			lastRun = currentMode
		sense.show_message("Teach, Learn and Make with Raspberry Pi", scroll_speed=.04, text_colour=(255,0,0))
		currentMode = 0
	if currentMode == 4:
		if lastRun is not currentMode:
			sense.show_message("ASK ME ANYTHING AND SHAKE!", scroll_speed=.03, text_colour=(255,0,0))
			lastRun = currentMode
			sense.show_letter("?", text_colour=(255,0,0))
		while currentMode == 4:
			x, y, z = sense.get_accelerometer_raw().values()
			if x > 2.5 or x < -2.5 or y > 2.5 or y < -2.5 or z > 2.5 or z < -2.5:
				sense.show_message(random.choice(replies), scroll_speed=.03, text_colour=(255,0,0))
				sense.show_letter("?", text_colour=(255,0,0))
			sleep(0.1)
			




