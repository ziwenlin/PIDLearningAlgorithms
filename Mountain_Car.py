import gym
import Settings
import Controllers


class MountainCar(Controllers.Environment_Controller):
    def get_action(self, observation: gym.core.ObsType) -> gym.core.ActType:
        output = 0
        if observation[1] < 0:
            output = cart_agent.get_output(observation[0], 0.6)
        elif observation[1] > 0:
            output = cart_agent.get_output(observation[0], -1.2)
        action = action_space(output)
        return action

    def get_reward(self, observation: gym.core.ObsType) -> float:
        reward = 0
        reward -= abs(observation[0] - 0.50)
        reward += abs(observation[1] * 100)
        return reward


def action_space(output):
    if output > 1:
        action = 2
    elif output < -1:
        action = 0
    else:
        action = 1
    return action


PID_CART = (0, 0, 0)
PID_CART = (-1.2978, -0.0252, -0.8364)
PID_CART = (-1.8086, -0.0327, -0.7587)

cart_agent = Controllers.Learning_PID_Controller(preset=PID_CART)
agent = cart_agent
agent.name = 'PID_CART'

env = gym.make('MountainCar-v0')
environment = Controllers.Environment(env, agent, MountainCar(env))

environment.start()
while environment.running:
    environment.step_episode()
    environment.step_end()
environment.stop()
