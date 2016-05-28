begin = 3
end = 5

i = 5
j = 8

data = []
for k in range(0,10):
	new = []
	for m in range(0,10):
		new.append(k)
	data.append(new)

for _list in data:
	print(_list)

for k in range(begin, end, 1):
	print (data[k][i:j+1])	