def representTBMK(value):
	response = value
	if value >= 1000000000000:
		response = str(round(value / 1000000000000, 1)) + "T"
	elif value >= 1000000000:
		response = str(round(value / 1000000000, 1)) + "B"
	elif value >= 1000000:
		response = str(round(value / 1000000, 1)) + "M"
	elif value >= 1000:
		response = str(round(value / 1000, 1)) + "K"

	return response


def obtain_float(value: str):
	if "," not in value and "." not in value:
		# check if its an integer
		if value.isnumeric():
			return float(value)
		else:
			return None

	# check if value is a valid number (first check if the string is compose of numbers and a single comma or dot, then check if the string can be converted to a float)
	if not value.replace(",", "").replace(".", "").isnumeric():
		return None

	# compose a float by splitting the string by comma or dot and joining it with a dot
	if "," in value:
		return float(".".join(value.split(",")))
	elif "." in value:
		return float(value)
	else:
		return None


def add_dots(value:int, dots_or_comma="dots"):
	# adds dots or commas to a number (IE: 1000000 becomes 1.000.000)
	if dots_or_comma != "dots" and dots_or_comma != "comma":
		return None

	value = str(value)

	if len(value) < 4:
		return value

	# reverse the string so it's easier to add the dots
	value = value[::-1]
	# split the string into groups of 3 characters
	value = [value[i:i+3] for i in range(0, len(value), 3)]
	# join the string with dots
	value = ".".join(value)
	# reverse the string again so it's back to normal
	value = value[::-1]

	return value