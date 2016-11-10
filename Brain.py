import random


class Neuron:

	START_THRESHOLD = 1
	THRESHOLD_CAP = 30
	DECAY_RATE = 3  # 1/X each decay  # Speed vs quality of learning
	ENCOURAGE_RATE = 10
	DISCOURAGE_RATE = 10

	def __init__(self):
		self.charge = 0
		self.fire_threshold = self.START_THRESHOLD + (random.random() * self.START_THRESHOLD)

	def add_charge(self, val):
		self.charge += val

	def get_fires(self):
		fires = self.charge // self.fire_threshold
		self.charge %= self.fire_threshold
		return fires

	def encourage(self):
		self.fire_threshold -= self.fire_threshold / self.ENCOURAGE_RATE

	def discourage(self):
		self.fire_threshold += self.START_THRESHOLD / self.DISCOURAGE_RATE
		if self.fire_threshold > self.THRESHOLD_CAP:
			self.fire_threshold = self.THRESHOLD_CAP

	def decay(self):
		self.charge -= self.fire_threshold / self.DECAY_RATE
		if self.charge < 0:
			self.charge = 0
