class Test:
	def __init__(self, source, destination):
		self.source = source
		self.destination = destination
		self.val = 0

	def charge(self):
		self.val += self.source

	def send(self):
		self.destination = self.charge


s = 1
d = 0
test = Test(s, d)
test.charge()
print(test.val)
test.send()
print(d)