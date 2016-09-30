import gym
import time

from Brain import Neuron

env = gym.make('CartPole-v0')
# print(env.action_space.n)
# print(len(env.observation_space.low))

input_count = len(env.observation_space.low)
action_count = env.action_space.n
neuron_count = input_count * 2 * action_count

episodes = 160
time_steps = 1000

neurons = []
for i in range(neuron_count):
	neurons.append(Neuron())

last_100_rewards = []
for e in range(episodes):
	print()
	print('STARTING EPISODE', e)
	observation = env.reset()
	total_reward = 0

	x = observation[0]
	x_dot = observation[1]
	angle = observation[2]
	angle_dot = observation[3]
	for t in range(time_steps):
		# time.sleep(1)
		# env.render()

		# print()
		# print('Thresholds to meet:')
		# print([n.fire_threshold for n in neurons])

		# action = env.action_space.sample()
		fired = []
		action = None
		while action is None:
			# Add charges based on input values
			for i in range(len(observation)):
				input = observation[i]
				input_neg = 0 if input > 0 else abs(input)
				input_pos = 0 if input < 0 else abs(input)
				neurons[2*i].add_charge(input_neg)
				neurons[2*i+1].add_charge(input_pos)

			# print('New Charges:')
			# print([n.charge for n in neurons])

			# Get fires from each neuron
			fires = [n.get_fires() for n in neurons]

			# Record fired neurons for alteration
			for f in range(len(fires)):
				fire_count = fires[f]
				neuron = neurons[f]
				if fire_count > 0:
					fired.append(neuron)

			# Determine action from neuron fires
			left = sum(fires[::2])
			right = sum(fires[1::2])
			if left >= right and left > 0:
				action = 0
			elif right >= left and right > 0:
				action = 1

		# print('action is', action)

		observation, reward, done, info = env.step(action)
		total_reward += reward

		new_x = observation[0]
		new_x_dot = observation[1]
		new_angle = observation[2]
		new_angle_dot = observation[3]
		# positive_result = abs(new_x) < abs(x) and abs(new_angle) < abs(angle) and abs(new_angle_dot) < abs(angle_dot) and abs(new_x_dot) < abs(x_dot)
		positive_result = abs(new_angle) < abs(angle) and abs(new_x_dot) < abs(x_dot)
		# positive_result = abs(new_angle) < abs(angle) and abs(new_x) < abs(x) and abs(new_x_dot) < abs(x_dot)
		x = new_x
		x_dot = new_x_dot
		angle = new_angle
		angle_dot = new_angle_dot

		# print('Positive Result:', positive_result)
		for neuron in fired:
			if positive_result:
				neuron.encourage()
			else:
				neuron.discourage()

		for neuron in neurons:
			neuron.decay()

		if done:
			# print('Episode finished after {0} timesteps'.format(t + 1))
			break

	print('Total Reward for this episode:', total_reward)
	last_100_rewards.append(total_reward)
	if len(last_100_rewards) > 100:
		last_100_rewards.pop(0)
	print('Average past 100 rewards:', sum(last_100_rewards) // len(last_100_rewards))
