import xinput
import time
from Tkinter import *
from socket import *  

HOST = '172.16.6.219'	# Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024			 # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
tcpCliSock.connect(ADDR) 

controller = xinput.XInputJoystick.enumerate_devices()[0]
input_buffer = .49
global forward 
forward = False
global reverse 
reverse = False
global isReversing
isReversing = False
global isForward
isForward = False
global left
left = False
global isLeft
isLeft = False
global right
right = False
global isRight
isRight = False

global cUp 
cUp = False
global cDown
cDown = False
global cLeft
cLeft = False
global cRight
cRight = False
global isCUp
isCUp = False
global isCDown
isCDown = False
global isCLeft
isCLeft = False
global isCRight
isCRight = False

spd = 200

def changeSpeed(speed):
	tmp = 'speed'
	global spd
	spd = speed
	data = tmp + str(spd)  # Change the integers into strings and combine them with the string 'speed'. 
	print 'sendData = %s' % data
	tcpCliSock.send(data)  # Send the speed data to the server(Raspberry Pi)

changeSpeed(50)

def quit_fun(event):
	tcpCliSock.send('stop')
	tcpCliSock.close()
	exit()

@controller.event
def on_button(button, pressed):
	if button == 14 and pressed == 1:
		changeSpeed(100)
	if button == 14 and pressed == 0:
		changeSpeed(50)
	if button == 5 and pressed == 1:
		quit_fun(button)

@controller.event
def on_axis(axis, value):
	global forward
	global reverse
	global left
	global right
	global cLeft
	global cRight
	global cUp
	global cDown
	if(axis == "right_trigger"):
		if(value > 0):
			forward = True
			reverse = False
		else:
			forward = False
	
	if(axis == "left_trigger"):
		if(value > 0):
			reverse = True
			forward = False
		else:
			reverse = False

	if(axis == "l_thumb_x"):
		if(value < -.1):
			left = True
			right = False
		else:
			left = False	

	if(axis == "l_thumb_x"):
		if(value > .1):
			right = True
			left = False
		else:
			right = False	

	if(axis == "r_thumb_x"):
		if(value > .1):
			cRight = True
			cLeft = False
		else:
			cRight = False
	
	if(axis == "r_thumb_x"):
		if(value < -.1):
			cLeft = True
			cRight = False
		else:
			cLeft = False
	
	if(axis == "r_thumb_y"):
		if(value > .1):
			cUp = True
			cDown = False
		else:
			cUp = False

	if(axis == "r_thumb_y"):
		if(value < -.1):
			cDown = True
			cUp = False
		else:
			cDown = False

while True:
	controller.dispatch_events()
	time.sleep(.01)
	if(reverse and not isReversing):
		tcpCliSock.send('backward')
		isReversing = True
	elif(forward and not isForward):
		tcpCliSock.send('forward')
		isForward = True
	elif((isReversing and not reverse) or (isForward and not forward)):
		tcpCliSock.send('stop')
		isReversing = False
		isForward = False
	
	if(left and not isLeft):
		tcpCliSock.send('left')
		isLeft = True
	elif(right and not isRight):
		tcpCliSock.send('right')
		isRight = True
	elif((isRight and not right) or (isLeft and not left)):
		tcpCliSock.send('home')
		isRight = False
		isLeft = False

	if(cLeft and not isCLeft):
		tcpCliSock.send('x-')
		isCLeft = True
	elif(cRight and not isCRight):
		tcpCliSock.send('x+')
		isCRight = True
	
	if(cUp and not isCUp):
		tcpCliSock.send('y+')
		isCUp = True
	elif(cDown and not isCDown):
		tcpCliSock.send('y-')
		isCDown = True
	# elif((isCRight and not cRight) or (isCLeft and not cLeft)):
	# 	tcpCliSock.send('xy_home')
	# 	isCLeft = False
	# 	isCRight = False
	