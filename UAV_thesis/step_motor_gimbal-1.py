import RPi.GPIO as GPIO
import time
import pigpio
import os

pi=pigpio.pi()
if not pi.connected:
    exit()

GPIO.setmode(GPIO.BOARD) #Set Raspberry Pi GPIO to BOARD numbering (as opposed to BCM)

ControlPin = {'x':[29,31,33,35],
		'y':[37,36,38,40]}

#for pin in ControlPin['x']:
#	GPIO.setup(pin, GPIO.OUT) #Set each pin to the OUTPUT mode
#	GPIO.output(pin,0) #Make sure they start as Off
for pin in ControlPin['y']:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,0)


#GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#Keeping this for when I add sensors / limit switches, useless for now

x_lim = float(180) #using type float() so we don't lose degrees over time from rounding
y_lim = float(180)

def checklimit(axis): #Returns true or false during go() to signal that the global limits are within/outside their set range
	if axis == 'x':
		return x_lim >= 360 or x_lim <= 0
	else:
		return y_lim >= 300 or y_lim <= 60

def updatelim(dir,axis): #update current angle of global limit vars based on current vector
	global x_lim
	global y_lim
	if dir == 1: #first number of sequence handed to updatelim is either 1 or 0 (forward or backwards) this determins direciton of vector
		x = 1
	if dir == 0:
		x = -1
	if axis == 'x':
		x_lim = x_lim + (.703125 * x) #these motors have 512 steps per revolution, each step is .703125 degrees
	if axis == 'y':
		y_lim = y_lim + (.703125 * x)

def go(seq,steps,speed,axis): #Takes the forward or backwards sequence, number of steps, delay between steps in microseconds, and axis to move the appropriate motors the desired number of steps 
	global x_lim
	global y_lim
	for i in range(steps): #in a typical keypress, this is 1 
		updatelim(seq[1][1],axis) #checks the first number of the current sequence to determine whether this is forward or backwards (see updatelim)
		if checklimit(axis) == True: #If the axis is outside it's limits, nope nope nope nope.
			break 
		for halfstep in range(8): #the sequences of 1's and 0's later on (f/b sequences) represent the on/off state of each output pin for a given axis. we have to switch this 8 times just to do one step
			for pin in ControlPin[axis]: #for each one of THOSE 8 sequences, we change the four output pins accordingly
				GPIO.output(pin, seq[halfstep][ControlPin[axis].index(pin)])
			time.sleep(float(speed)/1000) #we're moving a physical metal shaft here, so let's sleep and let it have a bit of time to catch up to what we're outputting, or else the motor will skip steps and not move anywhere.

def home(axis):
	global x_lim
	global y_lim
	if axis == 'x': #pretty simple. Monitor x and y axis angles until each is at 180 (striaght up).
		while x_lim != 180:
			if x_lim > 180:
				go(b,1,2,axis)
			if x_lim < 180:
				go(f,1,2,axis)	
	if axis == 'y':
		while y_lim != 180:
			if y_lim > 180:
				go(b,1,2,axis)
			if y_lim < 180:
				go(f,1,2,axis)
#---------------------------
f = [ [1,0,0,0], #each group in this sequence represents the state of four output pins.
	[1,1,0,0], #imagine the diagonal shape of 1's as the direction we're pushing magnetic current
	[0,1,0,0],
	[0,1,1,0],
	[0,0,1,0],
	[0,0,1,1],
	[0,0,0,1],
	[1,0,0,1] ]

b = [ [0,0,0,1],
	[0,0,1,1],
	[0,0,1,0],
	[0,1,1,0],
	[0,1,0,0],
	[1,1,0,0],
	[1,0,0,0],
	[1,0,0,1] ]


keymap = { 1:[b,1,2,'y'], #Created a dictionary of all key mappings, and direciton/steps/speed/axis for each key.
	   2:[f,1,2,'y'], #I've created more keys for a "two handed layout" to make moving the gimal in either 1 small step, or one step of 45 degrees.
	   3:[b,1,2,'x'],
	   4:[f,1,2,'x'],
	   5:[b,64,1,'y'],
	   6:[f,64,1,'y'],
	   7:[b,64,1,'x'],
	   8:[f,64,2,'x']}

#go(*keymap[6])
#home('y)

# mở terminal gõ : sudo systemctl enable pigpiod


def foo():
        foo.counter +=  1
foo.counter = 0
pre_degree = 0


def cbf(gpio,level,tick):
        global pre_degree
        
        if (level == 0) & (foo.counter == 1):
                cbf.y = tick
                foo.counter = 0
                dc = cbf.y - cbf.x
                #print(dc)
                degree = round((dc - 1100)*120/(750*0.703125))

                
                diff = degree - pre_degree
                if diff >=10:
                    print(diff)
                    go(f,diff,1,'y')
                    pre_degree = degree
                if diff <= -10:
                    print(diff)
                    go(b,abs(diff),1,'y')
                    pre_degree = degree



                
                #old_degree = degree
                #if diff >= 0:          
                #	go(b,diff,1,'y')
                #else:
                #	go(f,abs(diff),1,'y')

        if level == 1:
                foo()
                if foo.counter == 1:
                        cbf.x = tick
        #time.sleep(0.2)
                #endif
        #endif                               
#enddef cbf
#----------------------------






cb1=pi.callback(17,pigpio.EITHER_EDGE,cbf)   


     
		



