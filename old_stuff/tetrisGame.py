import gameEngine
import shapes
import time

def upButtonPressed():
	global tetris
	global pg
	tetris.flip(pg)
	pg.draw()


def rightButtonPressed():
	global tetris
	global pg
	tetris.goRight(pg)
	pg.draw()

def downButtonPressed():
	global tetris
	global pg
	tetris.goDown(pg)
	pg.draw()

def leftButtonPressed():
	global tetris
	global pg
	tetris.goLeft(pg)
	pg.draw()

gameEngine.upButtonPressed = upButtonPressed
gameEngine.rightButtonPressed = rightButtonPressed
gameEngine.downButtonPressed = downButtonPressed
gameEngine.leftButtonPressed = leftButtonPressed

class TetrisField(gameEngine.PlayGround2D):
	def __init__(self, y=4, x=4):
		super().__init__(y, x)

	def clearLine(self, line):
		for _value in self.playfield[line]:
			_value = 0

	def checkForLine(self):
		line = 0
		row = 0
		for _list in self.playfield:
			for _value in _list:
				if not _value == 3:
					break
				row += 1
				if row == self.sizeOfPlayField[1]:
					self.clearLine(line)
			line += 1

class TetrisShape(gameEngine.Sprite):
	def __init__(self):
		choice = gameEngine.getRandomNumber(0, len(shapes.shapes)-1)
		matrix = shapes.shapes[choice]
		super().__init__(matrix)

	def createNewShape(self):
		choice = gameEngine.getRandomNumber(0, len(shapes.shapes)-1)
		matrix = shapes.shapes[choice]
		self.shape = matrix

	def goDown(self,pg):
		lowest = self.getDownMostPartY()
		if lowest == pg.sizeOfPlayField[0]-1:
			self.createNewShape()
			self.draw(pg)
			#pg.draw()
			return 0
		
		for _list in self.shape:
			if pg.playfield[_list[0]+1][_list[1]] == _list[2] and not _list in self.shape:
				self.createNewShape()
				self.draw(pg)
				#pg.draw()
				return 0

		pg.clearThis(self.shape)
		for _list in self.shape:
			_list[0] += 1
		self.draw(pg)
		#pg.draw()

keyboard = gameEngine.catchInputFromKeyboard()
keyboard.start()

pg = TetrisField(16)
tetris = TetrisShape()

while 1:
	time.sleep(1)
	tetris.goDown(pg)
	pg.checkForLine()