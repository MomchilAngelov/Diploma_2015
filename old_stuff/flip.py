import gameEngine
import time

pg = gameEngine.PlayGround2D()
my_list = [
			[0,0,5],
			[1,0,5],
			[2,0,5],
			[2,1,5]
		]

my_sprite = gameEngine.Sprite(my_list)
my_sprite.draw(pg)
pg.draw()
time.sleep(2)

my_sprite.flip(pg)
pg.draw()

time.sleep(2)
my_sprite.flip(pg)
pg.draw()

time.sleep(2)
my_sprite.flip(pg)
pg.draw()
