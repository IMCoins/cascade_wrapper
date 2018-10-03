class Rectangle():
	def __init__(self, top, bot):
		self.top = top
		self.bot = bot

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

	def __repr__(self):
		return 'Point(x : {}, y : {})'.format(self.x, self.y)


