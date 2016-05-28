import time
import os
mylist = [
			[0,0,0,0,0],
			[0,0,0,0,0],
			[0,0,0,0,0],
			[0,0,0,0,0],
			[0,0,0,0,0]
		]

bit = [0,0]
lastposofbit = [0,0]
def prin(mylist):
	os.system("clear")
	for k in mylist:
		print(k)

prin(mylist)
time.sleep(1)
mylist[bit[0]][bit[1]] = 1
bit = [0,1]
while 1:
	time.sleep(1)
	mylist[lastposofbit[0]][lastposofbit[1]] = 0
	mylist[bit[0]][bit[1]] = 1
	prin(mylist)
	lastposofbit = bit
	bit[0] += 1
	bit[1] += 1
