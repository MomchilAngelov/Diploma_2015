#In here we will test our bumpable and movable objects :
import gameEngine
import time

score = 0

#controls for player1
def upButtonPressed():
	global sprite
	if sprite.direction == 3:
		pass
	else:
		sprite.direction = 1

def rightButtonPressed():
	global sprite
	if sprite.direction == 4:
		pass
	else:
		sprite.direction = 2

def downButtonPressed():
	global sprite
	if sprite.direction == 1:
		pass
	else:
		sprite.direction = 3

def leftButtonPressed():
	global sprite
	if sprite.direction == 2:
		pass
	else:
		sprite.direction = 4

def my_personal_interactor(key, player):
	print("Did it work tho")

gameEngine.upButtonPressed = upButtonPressed
gameEngine.rightButtonPressed = rightButtonPressed
gameEngine.downButtonPressed = downButtonPressed
gameEngine.leftButtonPressed = leftButtonPressed



mylist = [
		    #y,x,val[x][y]
			[0,0,8],
			[0,1,8],
			[0,2,8]
		]

class Snake(gameEngine.Sprite):
	def __init__(self, matrix, direction):
		super().__init__(matrix)
		self.direction = direction


	def move(self, pg, apple):
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
			#Eaten urself
			#No need for isInside, because
			#The third value (value in the field)
			#Is the same! 
			return 0

		if self.isInside(apple.shape):
			self.shape.append(_list)
			global score
			score += 1
			return 2
		
		del self.shape[0]
		self.shape.append(_list)
		return 1


pg = gameEngine.PlayGround2D()

#We want this too till 1st of feb
#huehue
#pg.music("my_music", "wav")

keyboard = gameEngine.catchInputFromKeyboard()
keyboard.start()
sprite = Snake(mylist, 2)
apple = gameEngine.Sprite()
apple.putAtRandomPlace(pg)

my_server = gameEngine.server()
my_server.ch.call_function_with_player = my_personal_interactor
my_server.start()

while True:
	data, addr = sock.recvfrom(40)
	all_clients.check_if_here(addr)
	data = data.decode()

	if data:
		print("{0} received from user {1}".format(data, all_clients.return_user_by_name(addr)))
		
		sock.sendto(data.encode(),(addr))
	else:
		break
print("You lost!")