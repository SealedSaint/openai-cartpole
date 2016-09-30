import random


class Neuron:
	START_THRESHOLD = 1
	DECAY_RATE = 10  # 1/10 each decay

	def __init__(self):
		self.charge = 0
		self.fire_threshold = self.START_THRESHOLD + random.random()

	def add_charge(self, val):
		self.charge += val

	def get_fires(self):
		fires = self.charge // self.fire_threshold
		self.charge %= self.fire_threshold
		return fires

	def encourage(self):
		self.fire_threshold -= self.fire_threshold / 10

	def discourage(self):
		self.fire_threshold += self.START_THRESHOLD

	def decay(self):
		self.charge -= self.fire_threshold / self.DECAY_RATE
		if self.charge < 0:
			self.charge = 0
