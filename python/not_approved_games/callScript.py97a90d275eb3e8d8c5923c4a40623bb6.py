'''
	Maybe i need a Queve in the gameEngine so i know which thread is going now and plan accordingly?
'''
import sys
import os
import threading
import gameEngine

class My_thread(threading.Thread):
	def __init__(self):
		super().__init__()
		

	def run(self):
		allFiles = gameEngine.getAllFiles("games")
		all_files_size = allFiles.__len__()
		
		if all_files_size == 0:
			print("No games downloaded yet!")
		else :	
			i = 0
			for file in allFiles:
				i += 1
				print("{0} {1}".format(i, file))
			while True:
				try:
					mode = int(input("Input:"))
				except ValueError: # just catch the exceptions you know!
					print ('That\'s not a number!')
				else:
					if 1 <= mode < all_files_size + 1: # this is faster
						break
					else:
						print ('Out of range. Try again')
			
			cwd = os.getcwd()
			os.chdir(cwd + "/games")
			os.system("cls")
			with open(allFiles[mode-1]) as python_file:
				code = compile(python_file.read(), python_file, 'exec')
				exec(code)
			os.chdir(cwd)
			input("Press any key to restart!")
			os.system("cls")

class My_other_thread(threading.Thread):
	def __init__(self):
		super().__init__()

	def run(self):
		gameEngine.getAllGames()
'''
get options - to download a game or to start one
implement the communication controller/console
implement the download game function
make a website in which you can upload games
	logic of website - upload a game to a temp folder
	and from there you can either put it in games or delete it (if not good or something)

	currently, our server will reside on localhost:80/

make a server script on the server that listens on certain port and gets 
filename and ID of console, and stores the ID of the console in the DB on the server
and gives back the file with filename!


'''
server = gameEngine.server()
server.start()

os.system("cls")

while True:
	print("1. Download a game")
	print("2. Play a game")
	print("3. Exit")
	while True:
		try:
			mode = int(input("Input:"))
		except ValueError: # just catch the exceptions you know!
			print ('That\'s not a number!')
		else:
			if 1 <= mode < 4: # this is faster
				break
			else:
				print ('Out of range. Try again')
	
	os.system("cls")
	if mode == 1:
		my_script = My_other_thread()
		my_script.start()
		my_script.join()

	if mode == 2:
		my_script = My_thread()
		my_script.start()
		my_script.join()
		
	if mode == 3:
		server.stop()
		sys.exit()	