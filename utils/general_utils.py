

def lower_first_letter(s:str) -> str:
	"""Return the string with the first letter in lowercase."""
	return s[0].lower() + s[1:]

if __name__ == '__main__':
	print(lower_first_letter("Hello")) #Expected: 'hello'