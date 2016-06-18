import gym, random, numpy as np
env = gym.make('CartPole-v0')
observation= env.reset()
reward, done = 0, False
eps = 0.1

class CartPoleBot(object):
  def __init__(self, action_space):
    self.action_space = action_space
    self.weights_left = [random.uniform(-0.05,0.05) for x in range(4)]
    self.weights_right = [random.uniform(-0.05,0.05) for x in range(4)]

  def calc_action(self, observa0tion, reward, done):
    q_left = observation.dot(self.weights_left)
    q_right = observation.dot(self.weights_right)
    if random.uniform(0,1) < 0.05:
      return env.action_space.sample()
    if q_left >= q_right:
      return 0
    else:
      return 1

  def update_weights(self, action, new_observation, old_observation, reward):
    if action == 0:
      diff = reward + new_observation.dot(self.weights_left) - old_observation.dot(self.weights_left)
      self.weights_left = [w + eps*diff*old_observation[i] for i, w in enumerate(self.weights_left)]
    if action == 1:
      diff = reward + new_observation.dot(self.weights_right) - old_observation.dot(self.weights_right)
      self.weights_right = [w + eps*diff*old_observation[i] for i, w in enumerate(self.weights_right)]

bot = CartPoleBot(env.action_space)
# env.monitor.start('cartpolev0', force=True)
for kk in range(200):
  observation = env.reset()
  for t in range(200):
      env.render()
      action = bot.calc_action(observation, reward, done)
      old_observation = observation
      observation, reward, done, info = env.step(action)
      bot.update_weights(action, observation, old_observation, reward)
      if done:
        print "it died after {}".format(t)
        break

# env.monitor.close()