import os

digits = []

with open(os.path.join("assets","one_million_digits_of_pi.txt")) as f:
	for text in f:
		for digit in text:
			digits.append(digit)

def search_in_pi(number):
	count = 1
	for i in range(len(digits) - len(number) + 1):
		find = True
		for j in range(len(number)):
			if not digits[i+j] == number[j]:
				find = False
		if find:
			return count
		count += 1

def main():

	to_search = input()

	if not search_in_pi(to_search) == None:
		print(f"{to_search} : is in {search_in_pi(to_search)} place")
	else:
		print(f"{to_search} not find in the first million digits of pi")

main()
