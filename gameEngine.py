import os
from os import listdir
from os.path import isfile, join
import threading
import time
import re
from copy import deepcopy
import random
#import pygame
from deepdiff import DeepDiff
import socket
import urllib.request
import sys
import csv
import json


def getAllGames(server):
	print("Name of game")
	print("================")
	address = "http://192.168.97.171:80/python/"
	all_games = []
	file = "games.csv"
	url = address + file
	file_name = "all_games.csv"
	i = 0
	urllib.request.urlretrieve(url, file_name)
	with open("all_games.csv") as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			i += 1
			print("{0} {1}".format(i, row[0]))
			all_games.append(row)
		print("{0} Exit".format(i+1))
		while True:
			try:
				data, addr = server.sock.recvfrom(40)
				data = data.decode()
				mode = int(data)
				if 1 <= mode < i+2: 
					break
				else:
					raise ValueError("Not in range!")
			except ValueError as valerr:
				print(valerr)
	if not mode == i+1:
		url = address + "games/" + all_games[mode-1][1]
		url = re.sub("\s+", "", url)
		print(url)
		file_name = "games/" + all_games[mode-1][0] + ".py"
		urllib.request.urlretrieve(url, file_name)
		os.system("clear")
		print("Game download complete! You downloaded: {0} from {1}".format(file_name, url))
	else:
		os.system("clear")

def getAllFiles(path, directory):
	os.chdir(directory)
	onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and f.split(".")[1] == "py"]
	return onlyfiles

def upButtonPressed():
	pass
def rightButtonPressed():
	pass 
def downButtonPressed():
	pass
def leftButtonPressed():
	pass
def gButtonPressed():
	pass
def getRandomNumber(arg1, arg2):
	return random.randint(arg1, arg2)

class all_clients_handler():
	def __init__(self, names = ['Player1','Player2','Player3','Player4']):
		self.data = []
		self.names = names

	def check_if_here(self, addr):
		for address in self.data:
			if addr != address[0]:
				pass
			else: 
				return 1
		new = []
		new.append(addr)
		new.append("{0}".format(self.names[0]))
		self.names.remove(self.names[0])
		self.data.append(new)

	def return_user_by_name(self, addr):
		for array in self.data:
			if array[0] == addr:
				return array[1]

	def call_function_with_player(self, data, player):
		pass

class server(threading.Thread):
	def __init__(self, all_clients_handler = all_clients_handler()):
		super().__init__()
		self.ch = all_clients_handler
		self.server_address = ('192.168.97.171', 12345)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(self.server_address)
		self.close = 0
		self.last_data = 0
		
	def run(self):
		while True:
			try:
				data, addr = self.sock.recvfrom(40)
				self.ch.check_if_here(addr)
				data = data.decode()

				if data:
					self.last_data = data
					self.ch.call_function_with_player(data, self.ch.return_user_by_name(addr))
					self.sock.sendto(data.encode(),(addr))

			except Exception:
				self.stop()

	def stop(self):
		try:
			self.sock.shutdown(socket.SHUT_RDWR)
			self.sock.close()
			self.close = 1
			sys.exit()
		except OSError:
			print("I dunno")
			sys.exit()
class gameServer(threading.Thread):
	def __init__(self, all_clients_handler = all_clients_handler()):
		super().__init__()
		self.ch = all_clients_handler
		self.server_address = ('192.168.97.171', 12346)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(self.server_address)
		self.close = 0
		
	def run(self):
		while True:
			try:
				data, addr = self.sock.recvfrom(40)
				self.ch.check_if_here(addr)
				data = data.decode()

				if data:
					self.ch.call_function_with_player(data, self.ch.return_user_by_name(addr))
					self.sock.sendto(data.encode(),(addr))
			except Exception:
				self.sock.shutdown(socket.SHUT_RDWR)
				self.sock.close()
				sys.exit()

	def stop(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()
		self.close = 1

#will not work on non-RPI system ;-;
#nomusic
class music_player(threading.Thread):
	def __init__(self, filename):
		threading.Thread.__init__(self)
		self.filename = filename

	def run(self):
		pygame.mixer.init()
		pygame.mixer.music.load(self.filename)
		pygame.mixer.music.play()

class PlayGround2D():
	def __init__(self, y=8, x=8, default = 0):
		self.sizeOfPlayField = [y,x]
		self.playfield = []
		self.old = [[]]
		self.default = default
		self.clean_data = []
		self.regex = re.compile(r"(?<=\[)(.*?)(?=\])")
		for i in range(0,y):
			new = []
			for j in range(0,x):
				new.append(default)
			self.playfield.append(new)

	def getDelta(self):
		self.clean_data = []

		delta = DeepDiff(self.playfield, self.old)
		#print(delta)
		delta = re.sub("'",'"',str(delta))
		data = json.loads(delta)

		if "values_changed" in data:
			for entry in data["values_changed"]:
				result = self.regex.findall(entry)
				self.clean_data.append([result[0], result[1], data["values_changed"][entry]['oldvalue']])
		
		if "iterable_item_added" in data:
			for entry in data["iterable_item_added"]:
				result = self.regex.findall(entry)
				try:
					iter(data["iterable_item_added"][entry])
					i = 0
					for value in data["iterable_item_added"][entry]:
						try:
							self.clean_data.append([result[0], result[1], value])
						except IndexError:
							i += 1
							self.clean_data.append([result[0], i, value])
				except TypeError:
					self.clean_data.append([result[0], result[1], data["iterable_item_added"][entry]])

		if "iterable_item_removed" in data:
			for entry in data["iterable_item_removed"]:
				result = self.regex.findall(entry)
				try:
					iter(data["iterable_item_removed"][entry])
					i = 0
					for value in data["iterable_item_removed"][entry]:
						try:
							self.clean_data.append([result[0], result[1], value])
						except IndexError:
							self.clean_data.append([result[0], i, value])
							i += 1
				except TypeError:
					self.clean_data.append([result[0], result[1], data["iterable_item_removed"][entry]])

	def draw(self):
		#implement sending to controller that will
		#draw stuff on a visualiser of some sort

		delta = self.getDelta()
		self.old = deepcopy(self.playfield)
		os.system("clear")
		for k in self.playfield:
			print(k)
		print("===Difference===")
		print(self.clean_data)
						
	def drawCentered(self, spriteRevolver,visionX=8,visionY=8):
		#The view field is 8:8+size of the sprite
		viewfieldx = visionX
		viewfieldy = visionY

		os.system("clear")
		leftView = spriteRevolver.getLeftMostPartX()

		rightView = spriteRevolver.getRightMostPartX()
		rightView = self.sizeOfPlayField[1] - 1 - rightView

		if rightView >= viewfieldx/2 and leftView >= viewfieldx/2:
			view1 = viewfieldx/2
			view2 = viewfieldx/2
			beginX = leftView - view1
			endX = spriteRevolver.getRightMostPartX() + view2
		if rightView < viewfieldx/2:
			view1 = viewfieldx - rightView
			view2 = rightView
			beginX = leftView - view1
			endX = view2 + spriteRevolver.getRightMostPartX()
		if leftView < viewfieldx/2:
			view1 = leftView
			view2 = viewfieldx - leftView
			beginX = 0
			endX = spriteRevolver.getRightMostPartX() + view2

		topView = spriteRevolver.getTopMostPartY()

		downView = spriteRevolver.getDownMostPartY()
		downView = self.sizeOfPlayField[0] - 1 - downView

		if downView >= viewfieldy/2 and topView >= viewfieldy/2:
			view3 = viewfieldy/2
			view4 = viewfieldy/2
			beginY = topView - viewfieldy/2
			endY = spriteRevolver.getDownMostPartY() + 4
		if downView < viewfieldy/2:
			view4 = downView
			view3 = viewfieldy - downView
			beginY = topView - view3
			endY = spriteRevolver.getDownMostPartY() + view4
		if topView < viewfieldy/2:
			view3 = topView
			view4 = viewfieldy - topView
			beginY = 0 
			endY = spriteRevolver.getDownMostPartY() + view4

		for i in range(beginY, endY, 1):
			print (self.playfield[i][beginX:endX])		


	def clearThis(self, matrix):
		for _list in matrix:
			try:
				self.playfield[_list[0]][_list[1]] = 0
			except IndexError:
				pass
		
	def clear(self):
		arg1 = self.sizeOfPlayField[0]
		arg2 = self.sizeOfPlayField[1]
		self.playfield = []
		for i in range(0,arg1):
			new = []
			for j in range(0,arg2):
				new.append(self.default)
			self.playfield.append(new)

	def drawSpriteOnRandomWall(self, sprite):
		pass

class PlayGround3D():
	#?
	pass

class movable_handler(threading.Thread):
	def __init__(self, pg, bumpable_handler,timer=0.5):
		super().__init__()
		self.data = []
		self.pg = pg
		self.is_alive = 1
		self.sleep_timer = timer
		self.bumpable_handler = bumpable_handler

	def add_object(self, obj):
		self.data.append(obj)

	def delete_object(self, obj):
		self.data.remove[obj]

	def run(self):
		while self.is_alive:
			for _object in self.data:
				_object.move(self.pg)
			self.bumpable_handler.check_all_bumpable_objects()
			self.pg.draw()
			time.sleep(self.sleep_timer)
		sys.exit()

	def shutdown(self):
		self.is_alive = 0

class bumpable_handler(threading.Thread):
	def __init__(self, pg):
		super().__init__()
		self.data = []
		self.pg = pg

	def check_all_bumpable_objects(self):
		object_bumpable_list = self.data
		#counter so we dont have to check already checked elements
		counter = 0
		#for each element in the array
		for _object in object_bumpable_list:
			counter += 1
			'''
			for each element in the array that are infront of our own. This makes
			the game less buggy - we cant check against the object itself,
			which will return true always. We also make the checking faster this way 
			'''
			for other_objects in object_bumpable_list[counter:]:
				#If the object inside another object (returns One if inside, 0 otherwise)
				if _object.is_inside(other_objects.shape):
					self.object_collision(other_objects, _object)
		
	def object_collision(self, other_objects, _object):
		pass

	def add(self, _object):
		self.data.insert(0, _object)

	def shutdown(self):
		pass

class Sprite():
	def __init__(self, _type, matrix=[[0,0,5]]):
		self.shape = matrix
		#self.bullet = bullet
		self.faceDirection = 2 
		self.type = _type

	def out_of_bound(self, pg):
		pass

	def fire(self, pg, prHandler, speed=1, power=1):
		pass
		#proj = Projectile(self.bullet, speed, self.faceDirection, pg, self.shape[0][0], self.shape[0][1], power)
		#prHandler.addObject(proj)

	def getLeftMostPartX(self):
		leftMostX = 15
		for _list in self.shape:
			if _list[1] < leftMostX:
				leftMostX = _list[1]
		return leftMostX

	def getRightMostPartX(self):
		rightMostX = 0
		for _list in self.shape:
			if _list[1] > rightMostX:
				rightMostX = _list[1]
		return rightMostX

	def getDownMostPartY(self):
		downMostY = 0
		for _list in self.shape:
			if _list[0] > downMostY:
				downMostY = _list[0]
		return downMostY

	def getTopMostPartY(self):
		upMostY = 100
		for _list in self.shape:
			if _list[0] < upMostY:
				upMostY = _list[0]
		return upMostY

	def draw(self, pg, x=0, y=0):
		for _list in self.shape:
			try:
				_list[1] += x
				_list[0] += y
				pg.playfield[_list[0]][_list[1]] = _list[2]
			except IndexError:
				self.out_of_bound(pg)
			else:
				if _list[1] < 0 or _list[0] < 0:
					self.out_of_bound(pg)

	def goLeft(self, pg, speed=1):
		self.faceDirection = 4
		junky = self.getLeftMostPartX()
		if junky < speed:
			return 0

		pg.clearThis(self.shape)
		for _list in self.shape:
			_list[1] -= speed
		self.draw(pg)
		#pg.draw()

	def goRight(self, pg, speed=1):
		self.faceDirection = 2
		maxRight = self.getRightMostPartX()
		if maxRight < pg.sizeOfPlayField[1]-speed:
			return 0
		pg.clearThis(self.shape)
		for _list in self.shape:
			_list[1] += speed
		self.draw(pg)
		#pg.draw()

	def goDown(self, pg, speed=1):
		self.faceDirection = 3
		maxDown = self.getDownMostPartY()
		if maxDown < pg.sizeOfPlayField[0]-speed:
			return 0
		pg.clearThis(self.shape)
		for _list in self.shape:
			_list[0] += speed
		self.draw(pg)
		#pg.draw()

	def goUp(self, pg, speed=1):
		self.faceDirection = 1
		maxUp = self.getTopMostPartY()
		if maxUp < speed:
			return 0
		pg.clearThis(self.shape)
		for _list in self.shape:
			_list[0] -= speed
		self.draw(pg)
		#pg.draw()		

	def is_inside(self, matrix):
		for k in self.shape:
			for m in matrix:
				if m[0] == k[0] and m[1] == k[1]:
					return 1
		return 0

	def move(self, pg):
		pass

	def putAtRandomPlace(self, pg):
		while 1:
			y = random.randint(1-pg.sizeOfPlayField[0], pg.sizeOfPlayField[0]-1)
			x = random.randint(1-pg.sizeOfPlayField[1], pg.sizeOfPlayField[1]-1)
			size = len(self.shape)
			counter = 0
			for _list in self.shape:
				if _list[0] + y > pg.sizeOfPlayField[0]-1 or _list[0] + y < 0 or _list[1] + x > pg.sizeOfPlayField[1]-1 or _list[1] + x < 0:
					break
				if pg.playfield[_list[0]+y][_list[1]+x] == pg.default:
					counter += 1
				else:
					break
			if counter == size:
				self.draw(pg, x, y)
				break

	def flip(self, pg, direction=0):
		#Flip point is a list of 2 values (3 in xyz), and direction is either left or right
		newShape = self.getNewArray(pg)

		if newShape == 1:
			return
		else:	
			pg.clearThis(self.shape)
			self.shape = newShape
			self.draw(pg)
			#pg.draw()

	def findFlipPoint(self):
		#analyze shape and find the list with highest y then lowest x
		#[y, x, value]
		my_list = []
		highestY = 0
		lowestX = 0
		for _list in self.shape:
			if highestY < _list[0]:
				highestY = _list[0]
		my_list.append(highestY)

		for _list in self.shape:
			if _list[0] == 2:
				if lowestX > _list[1]:
					lowestX = _list[1]
			else:
				pass
		my_list.append(lowestX)
		return my_list

	def getNewArray(self, pg):
		flipPoint = self.findFlipPoint()
		newShape = []
		refferenceX = flipPoint[1]
		refferenceY = flipPoint[0]

		for _list in self.shape:
			diffY = _list[0] - refferenceY
			diffX = _list[1] - refferenceX

			if diffY == 0:
				newX = refferenceX	
			else:
				newX = refferenceX - diffY
				
			if diffX == 0:
				newY = refferenceY
			else:
				newY = refferenceY + diffX

			if newX < 0 or newX > pg.sizeOfPlayField[1]-1 or newY < 0 or newY > pg.sizeOfPlayField[0]-1:
				return 1	
			newShape.append([newY, newX, _list[2]])
		return newShape

class Projectile(Sprite):
	def __init__(self, matrix, speed, direction, pg, x, y, power):
		self.active = 1
		for _list in matrix:
			_list[0] + y
			_list[1] + x
		super().__init__(matrix)
		self.speed = speed
		self.power = power
		self.faceDirection = direction
		self.draw(pg)

	def move(self, pg):
		#if wall is struck, active == 0
		if self.faceDirection == 3:
			self.goDown(pg, self.speed)
		if self.faceDirection == 1:
			self.goUp(pg, self.speed)
		if self.faceDirection == 2:
			self.goRight(pg, self.speed)
		if self.faceDirection == 4:
			self.goLeft(pg, self.speed)
			
class catchInputFromKeyboard(threading.Thread):
	def __init__(self):
	    threading.Thread.__init__(self)
	
	def run(this):
		import termios, fcntl, sys
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
		            	upButtonPressed()
		            elif c=="B":
		            	downButtonPressed()
		            elif c=="D":
		            	leftButtonPressed()
		            elif c=="C":
		            	rightButtonPressed()
		            elif c=="g":
		            	gButtonPressed()
		        except IOError: pass
		finally:
		    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
