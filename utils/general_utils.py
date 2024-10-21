import os
import sys, os
import math
from fractions import Fraction
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *


def is_float_or_fraction(value:str):
	try:
		return float(Fraction(value))
	except ValueError:
		return False

def lower_first_letter(s:str) -> str:
	"""Return the string with the first letter in lowercase."""
	return s[0].lower() + s[1:]

def isEven(number:int) -> bool:
	return number % 2 == 0

def rotate_sequence(old_sequence, index:int) -> list | tuple:
	new_sequence = old_sequence[index:] + old_sequence[:index]
	return new_sequence

def repeat_values_to_size(list_size:int, *values):
	divided_size = math.ceil(list_size / len(values))
	values_list = []
	for value in values:
		values_list += [value] * divided_size
	return values_list

if __name__ == '__main__':
	#size = 3
	print(repeat_values_to_size(-1, 1, 2, True))
