import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import gameEngine

class myBumpableHandler(gameEngine.bumpable_handler):
	def __init__(self, pg):
		super().__init__(pg)

	def object_collision(self, object1, object2):
		if object1._type == "Snake" and object2._type == "Apple":
			object1.grow()
			object2.respawn(self.pg)
			print("allahu akbar")
		if object1._type == "Apple" and object2._type == "Snake":
			object1.respawn(self.pg)
			object2.grow()
			print("allahu akbar")

class Snake(gameEngine.Sprite):
	def __init__(self, _type,direction, matrix):
		super().__init__(_type, matrix)
		self.direction = direction
		self.last_block = [0,0,0]
		self._type = _type

	def move(self, pg):
		pg.clearThis(self.shape)
		curr = self.shape[-1]
		# 1
		#4 2
		# 3
		# [0]-Y [1]-X [2]-Value
		direction = self.direction
		if direction == 2:
			_list = [curr[0],curr[1]+1,curr[2]]
		elif direction == 3:
			_list = [curr[0]+1,curr[1],curr[2]]
		elif direction == 4:
			_list = [curr[0], curr[1]-1,curr[2]]
		elif direction == 1:
			_list = [curr[0]-1, curr[1], curr[2]]		
		
		if _list in self.shape:
			global game_server
			game_server.stop()
			sys.exit()

		self.last_block = self.shape[0]
		del self.shape[0]
		self.shape.append(_list)
		e_code = self.draw(pg)
		if e_code == 0:
			global game_server
			game_server.stop()
			sys.exit()

	def draw(self, pg, x=0, y=0):
		for _list in self.shape:
			try:
				_list[1] += x
				_list[0] += y
				pg.playfield[_list[0]][_list[1]] = _list[2]
			except IndexError:
				return 0
	
	def grow(self):
		self.shape.insert(0, self.last_block)

class Apple(gameEngine.Sprite):
	def __init__(self, _type,  matrix=[[5,2,3]]):
		super().__init__(type, matrix)
		self._type = _type

	def respawn(self, pg):
		self.putAtRandomPlace(pg)

class myPlayersHandler(gameEngine.all_clients_handler):
	def __init__(self, names = ['Player1','Player2','Player3','Player4']):
		super().__init__(names)

	def call_function_with_player(self, data, player):
		print("Called from player {0} with data {1}".format(player,data))
		global snake
		if player == self.names[0]:
			if data == "0" and snake.direction == 4:
				pass
			else:
				snake.direction = 2
			if data == "90" and snake.direction == 3:
				pass
			else: 
				snake.direction = 1
			if data == "180" and snake.direction == 2:
				pass
			else: 
				snake.direction = 4
			if data == "270" and snake.direction == 1:
				pass
			else:
				snake.direction = 3

snake_matrix = [[0,0,5],[0,1,5],[0,2,5]]

pg = gameEngine.PlayGround2D(13,15)

my_player_handler = myPlayersHandler(["Pesho","Sahso","Ivon","Ivan"])
game_server = gameEngine.gameServer(my_player_handler)
game_server.start()


apple = Apple("Apple")

snake = Snake("Snake", 3, snake_matrix)

bumpable_handler = myBumpableHandler(pg)
bumpable_handler.add(snake)
bumpable_handler.add(apple)

apple.respawn(pg)
snake.draw(pg)
apple.draw(pg)
pg.draw()

movable_handler = gameEngine.movable_handler(pg, bumpable_handler)
movable_handler.add_object(snake)
movable_handler.run()


while 1:
	pass