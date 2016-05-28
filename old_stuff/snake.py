import os
import time
import random
import threading

class catchInputFromKeyboard(threading.Thread):
	def __init__(self):
	    threading.Thread.__init__(self)
	
	def run(this):
		import termios, fcntl, sys, os
		fd = sys.stdin.fileno()

		oldterm = termios.tcgetattr(fd)
		newattr = termios.tcgetattr(fd)
		newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
		termios.tcsetattr(fd, termios.TCSANOW, newattr)

		oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

		try:
		    while 1:
		        try:
		            c = sys.stdin.read(1)
		            if c == "A":
		            	global direction
		            	if direction == 1:
		            		continue
		            	else:
		            		direction = 1
		            elif c=="B":
		            	global direction
		            	if direction == 3:
		            		continue
		            	else:
		            		direction = 3
		            elif c=="D":
		            	global direction
		            	if direction == 4:
		            		continue
		            	else:
		            		direction = 4
		            elif c=="C":
		            	global direction
		            	if direction == 2:
		            		continue
		            	else:
		            		direction = 2
		        except IOError: pass
		finally:
		    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

class playField():
	def __init__(self, arg1=8, arg2=8):
		self.sizeOfPlayField = [arg1,arg2]
		self.playfield = []
		for i in range(0,arg1):
			new = []
			for j in range(0,arg2):
				new.append(0)
			self.playfield.append(new)

	def printme(self):
		os.system("clear")
		for k in self.playfield:
			print(k)

	def createApple(self, snake):
		counter=1
		checker = [10,10]
		while checker in snake.shape or counter==1:
			counter+=1
			number1 = random.randint(0,self.sizeOfPlayField[0]-1)
			number2 = random.randint(0,self.sizeOfPlayField[1]-1)
			checker = [number1, number2]
		
		self.applex = number1
		self.appley = number2

		self.putThereApple(number1,number2,2)

	def putThereApple(self, x, y, value):
		self.playfield[x][y] = value

	def clearField(self):
		arg1 = self.sizeOfPlayField[0]
		arg2 = self.sizeOfPlayField[1]

		self.playfield = []
		for i in range(0,arg1):
			new = []
			for j in range(0,arg2):
				new.append(0)
			self.playfield.append(new)		

	def draw(self, snake):
		self.clearField()
		self.putThereApple(self.applex, self.appley, 2)
		for k in snake.shape:
			self.playfield[k[1]][k[0]] = 1
		self.printme() 

class snake():
	def __init__(self):
		self.shape = []

		post = [0,0]
		self.shape.append(post)

		post = [1,0]
		self.shape.append(post)

		post = [2,0]
		self.shape.append(post)

		
		 
		#	1
		#  4 2
		#	3
	def step(self, pf):
		global direction
		currpost = self.shape[-1]
		if direction == 1:
			mylist = [currpost[0],currpost[1]-1]
			if mylist in self.shape:
				global play
				play = 0
			self.shape.append(mylist)
			if pf.playfield[mylist[1]][mylist[0]] == 2:
				pf.createApple(self)
				pf.draw(self)
			else:
				del self.shape[0]
				pf.draw(self)

		elif direction == 2:
			mylist = [currpost[0]+1,currpost[1]]
			if mylist in self.shape:
				global play
				play = 0
			self.shape.append(mylist)
			if pf.playfield[mylist[1]][mylist[0]] == 2:
				pf.createApple(self)
				pf.draw(self)
			else:
				del self.shape[0]
				pf.draw(self)

		elif direction == 3:
			mylist = [currpost[0],currpost[1]+1]
			if mylist in self.shape:
				global play
				play = 0
			self.shape.append(mylist)
			if pf.playfield[mylist[1]][mylist[0]] == 2:
				pf.createApple(self)
				pf.draw(self)
			else:
				del self.shape[0]
				pf.draw(self)

		else:
			mylist = [currpost[0]-1,currpost[1]]
			if mylist in self.shape:
				global play
				play = 0
			self.shape.append(mylist)
			if pf.playfield[mylist[1]][mylist[0]] == 2:
				pf.createApple(self)
				pf.draw(self)
			else:
				del self.shape[0]
				pf.draw(self)
				

direction = 2
play = 1

pf = playField()
snake = snake()
keyboard = catchInputFromKeyboard()
keyboard.start()
pf.createApple(snake)
pf.draw(snake)

while play:
	time.sleep(0.5)
	snake.step(pf)

print("You lost ;-;")