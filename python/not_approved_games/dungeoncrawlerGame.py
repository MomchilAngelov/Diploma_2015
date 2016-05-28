import gameEngine
import time

def upButtonPressed():
	global my_sprite
	global pg
	my_sprite.goUp(pg)
	my_sprite.draw(pg)
	pg.drawCentered(my_sprite)

def rightButtonPressed():
	global my_sprite
	global pg
	my_sprite.goRight(pg)
	my_sprite.draw(pg)
	pg.drawCentered(my_sprite)

def downButtonPressed():
	global my_sprite
	global pg
	my_sprite.goDown(pg)
	my_sprite.draw(pg)
	pg.drawCentered(my_sprite)

def leftButtonPressed():
	global my_sprite
	global pg
	my_sprite.goLeft(pg)
	my_sprite.draw(pg)
	pg.drawCentered(my_sprite)

def gButtonPressed():
	global my_sprite
	global bullets
	global pg
	my_sprite.fire(pg,bullets)

gameEngine.upButtonPressed = upButtonPressed
gameEngine.rightButtonPressed = rightButtonPressed
gameEngine.downButtonPressed = downButtonPressed
gameEngine.leftButtonPressed = leftButtonPressed
gameEngine.gButtonPressed = gButtonPressed

my_list = [
			[0,0,5],
			[0,1,5],
			[1,0,5],
			[1,1,5]
		]

my_treasure = [
				[0,0,3],
				[0,1,3],
				[1,0,3],
				[1,1,3]
			]

keyboard = gameEngine.catchInputFromKeyboard()
keyboard.start()

bullets = gameEngine.ProjectileHandler()
bullets.start()

pg = gameEngine.PlayGround2D(32,32,1)
my_sprite = gameEngine.Sprite(my_list)
my_sprite.draw(pg)
pg.drawCentered(my_sprite)

for i in xrange(5):
	my_treasure = gameEngine.Sprite(my_treasure)
	my_treasure.draw(pg)


while 1:
	time.sleep(0.5)
	pg.drawCentered(my_sprite)