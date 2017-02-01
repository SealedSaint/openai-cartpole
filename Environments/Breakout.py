import gym
import numpy as np
from Brain import Neuron

env = gym.make("Breakout-v0")

EPISODES = 1
TIME_STEPS = 1000
RGB_MAX = 255

# Convert the size (x, y, 3) rgb pixel array into a size (x, y) array with
# grey values scaled between 0 and 1
def normalize(rgbOb):
	rgb = np.array(rgbOb)
	return np.dot(rgb, [.3, .6, .1]) / RGB_MAX

for e in range(EPISODES):
	print()
	print('STARTING EPISODE', e+1)
	observation = env.reset()

	''' NOTES:
		Observations is 210x160x3 with 210 rows of pixels, 160 columns of pixels, and 3 color values (rgb).
			Top to bottom, left to right, r-g-b.
		Reward is 0 except when score increases - then 1.
	'''
	for t in range(TIME_STEPS):
		env.render()

		action = env.action_space.sample()  # Random action
		observation, reward, done, info = env.step(action)
		normOb = normalize(observation)
		# print(normOb[100])

		# This tells us if the simulation has ended
		if done:
			print('Episode finished after {0} timesteps'.format(t + 1))
			break