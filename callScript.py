import sys
import os
import threading
import gameEngine

class My_thread(threading.Thread):
	def __init__(self, directory):
		super().__init__()
		self.directory = directory

	def run(self):
		print("Name of game")
		print(self.directory)
		print("================")
	
		allFiles = gameEngine.getAllFiles("games", self.directory)
		all_files_size = allFiles.__len__()
		
		if all_files_size == 0:
			print("No games downloaded yet!")
		else:	
			i = 0
			for file in allFiles:
				i += 1
				print("{0} {1}".format(i, file))
			
			while True:
				try:
					data, addr = server.sock.recvfrom(40)
					server.ch.check_if_here(addr)
					data = data.decode()

					if data:
						try:
							mode = int(data)
						except ValueError:
							pass
						else:
							if 1<= mode < all_files_size + 1:
								break
							else:
								pass
				except OSError:
					sys.exit()

			os.chdir(self.directory + "/games")
			os.system("clear")
			with open(allFiles[mode-1]) as python_file:
				code = compile(python_file.read(), python_file, 'exec')
				exec(code)
			
			os.chdir(self.directory)
			del sys.path[1]
			while True:
				try:
					data, addr = server.sock.recvfrom(40)
					server.ch.check_if_here(addr)
					data = data.decode()

					if data:
						break
						
				except OSError:
					sys.exit()
											
			os.system("clear")

class My_other_thread(threading.Thread):
	def __init__(self):
		super().__init__()

	def run(self):
		gameEngine.getAllGames()


server = gameEngine.server()
curr_directory = os.getcwd() 

while True:
	print("1. Download a game")
	print("2. Play a game")
	print("3. Exit")
	while True:
		try:
			data, addr = server.sock.recvfrom(40)
			server.ch.check_if_here(addr)
			data = data.decode()

			if data:
				if data == "2":
					mode = 2
					break

				if data == "1":
					mode = 1
					break

				if data == "3":
					mode = 3
					break

		except OSError:
			sys.exit()

	os.system("clear")
	if mode == 1:
		my_script = My_other_thread()
		my_script.start()
		my_script.join()

	if mode == 2:
		my_script = My_thread(curr_directory)
		my_script.start()
		my_script.join()
		
	if mode == 3:
		server.stop()
		sys.exit()	