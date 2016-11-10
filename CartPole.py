import gym

from Brain import Neuron

env = gym.make('CartPole-v0')
# print(env.action_space.n)
# print(len(env.observation_space.low))

input_count = len(env.observation_space.low)
action_count = env.action_space.n
neuron_count = input_count * 2 * action_count

EPISODES = 5000
TIME_STEPS = 1000

neurons = []
for i in range(neuron_count):
	neurons.append(Neuron())

STEPS_TO_FAIL = 25  # 20-30

last_100_rewards = []
for e in range(EPISODES):
	print()
	print('STARTING EPISODE', e)
	observation = env.reset()
	total_reward = 0
	prev_fired = []

	for t in range(TIME_STEPS):
		# print()
		# print('Thresholds to meet:')
		# print([n.fire_threshold for n in neurons])

		# action = env.action_space.sample()
		fired = []
		action = None
		loop_count = 0
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
					# for i in range(int(fire_count)):
					# neuron.encourage()  # If a neuron fired, encourage that behavior

			# Determine action from neuron fires
			left = sum(fires[::2])  # The even-indexed neurons
			right = sum(fires[1::2])  # The odd-indexed neurons
			if left >= right and left > 0:
				action = 0
			elif right >= left and right > 0:
				action = 1

			loop_count += 1

		# print('action is', action)

		observation, reward, done, info = env.step(action)
		total_reward += reward

		# Update the neurons
		prev_fired.append(fired)
		if len(prev_fired) > STEPS_TO_FAIL:  # TIME_STEP_MEMORY:
			removed_fired = prev_fired.pop(0)
			for neuron in removed_fired:
				neuron.encourage()
				# neuron.encourage()

		# Always decay the neurons at each step
		for neuron in neurons:
			neuron.decay()

		# This tells us if the simulation has ended
		if done:
			# print('Episode finished after {0} timesteps'.format(t + 1))
			bad_fires = prev_fired[-STEPS_TO_FAIL:]
			# if len(prev_fired) > 50: print('Length of bad fires:', len(bad_fires))
			for fired in bad_fires:
				for neuron in fired:
					neuron.discourage()

			# if e >= 100:
			# 	TIME_STEP_MEMORY = max(sum(last_100_rewards) // len(last_100_rewards), TIME_STEP_MEMORY)

			break

	print('Total Reward for this episode:', total_reward)
	last_100_rewards.append(total_reward)
	if len(last_100_rewards) > 100:
		last_100_rewards.pop(0)
	print('Average past 100 rewards:', sum(last_100_rewards) // len(last_100_rewards))
	print('Total Neuron Threshold:', int(sum([neuron.fire_threshold for neuron in neurons])))
	print('Hightest Threshold:', max([n.fire_threshold for n in neurons]))
	print('Neurons at 30:', len(list(filter(lambda n: n.fire_threshold == 30, neurons))))
	print('Neurons below 1:', len(list(filter(lambda n: n.fire_threshold < 1, neurons))))
