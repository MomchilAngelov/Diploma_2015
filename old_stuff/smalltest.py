import random

number1 = random.randint(0,5)
number2 = random.randint(0,5)
i = [number1, number2] 

j = [
		[1,2],
		[2,3]
	]

while i in j:
	number1 = random.randint(0,5)
	number2 = random.randint(0,5)
	i = [number1, number2] 
	print("sad")