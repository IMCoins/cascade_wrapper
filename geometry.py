class Rectangle():
	def __init__(self, top, bot):
		self.top = top
		self.bot = bot

	def __eq__(self, other):
		return self.top == other.top and self.bot == other.bot

	def __repr__(self):
		return 'Rectangle(top: {}, bot: {})'.format(self.top, self.bot)

	@property
	def width(self):
		return abs(self.top.x - self.bot.x)

	@property
	def height(self):
		return abs(self.top.y - self.bot.y)

	@property
	def area(self):
		return self.width * self.height

	def get_common_area(self, other):
		"""	Compares the surface of the rectangle with the other rectangle
			inserted as parameter. Then, returns the 
			overlapping rectangle area.
		"""
		top	= Point(max(self.top.x, other.top.x), min(self.top.y, other.top.y))
		bot	= Point(min(self.bot.x, other.bot.x), max(self.bot.y, other.bot.y))
		return Rectangle(top, bot).area

class Point():
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __repr__(self):
		return 'Point(x : {}, y : {})'.format(self.x, self.y)

if __name__ == '__main__':
	top_p1 = Point(3, 7)
	bot_p1 = Point(7, 3)
	rect_1 = Rectangle(top_p1, bot_p1)

	top_p2 = Point(1, 6)
	bot_p2 = Point(6, 1)
	rect_2 = Rectangle(top_p2, bot_p2)

	top_p3 = Point(4, 5)
	bot_p3 = Point(5, 6)
	rect_3 = Rectangle(top_p3, bot_p3)

	print(rect_2.area)
	print(rect_1.get_common_area(rect_2))

	# print(rect_1)
	# print(rect_1.width, rect_1.height, rect_1.area)
	# rect_1.bot = bot_p3

	# print(rect_1)
	# print(rect_1.width, rect_1.height, rect_1.area)


