import os
import shapes
import random
import time
print("Hello World!")

class playField():
	def __init__(self, arg1=8, arg2=8):
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

	def draw(self, matrix, x=0, y=0): 
		row = 0
		playfieldx = x
		playfieldy = y 	
		for k in matrix:
			for v in k:
				self.playfield[row+playfieldx][v+playfieldy] = matrix[row][v]
			row += 1

	def losscondition(self):
		for k in range(0, len(self.playfield[0])):
			if self.playfield[1][k] == 1:
				return 1
		return 0	

	def deletethis(self,row,col):
		self.playfield[row][col] = 0


class fallingBlock():

	def __init__(self):
		number = random.randint(0,shapes.numberofshapes)
		self.shape = shapes.shapes[number] 
		self.active = 1
		self.y = 0
		#the left-most position, in this case- right next to the left wall, making it 0
		self.x = 0
		
		self.xaxis = []
		self.xaxisfirst = []
		for k in self.shape[len(self.shape)-1]:
			self.xaxis.append(k)
		for k in self.shape[0]:
			self.xaxisfirst.append(k)

	def deletethisshape(self, pf):
		row = 0
		for k in self.shape:
			for v in k:
				if self.shape[row][v] == 1:
					pf.deletethis(row+self.x, v+self.y)
			row += 1 

	def godown(self, pf):
		self.deletethisshape(pf)
		self.y += 1
		pf.draw(self.shape, self.y, self.x)

	def killBlockCondition(self, pf):
		movedLeft = self.x
		if pf.playfield[self.y] == len(pf.playfield):
			return 1
			#The block hit the bottom shit

		mylist = pf.playfield[self.y+1]
		for v in range(movedLeft, movedLeft + len(self.xaxis)):
			if mylist[v] == 1 and self.xaxis[v] == 1:
				return 1
			#The block hit another block
		return 0
		#The block is fine
pf = playField()
pf.printme()
while 1:
	if pf.losscondition():
		break
	time.sleep(1)

	bl = fallingBlock()
	pf.draw(bl.shape, bl.y)
	pf.printme()

	while 1:
		time.sleep(1)
		if not bl.killBlockCondition(pf):
			bl.godown(pf)
			pf.printme()
		else:
			break
os.system("clear")
print("You lost :(")