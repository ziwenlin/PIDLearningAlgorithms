import Controllers
import Settings
import gym

PRESET_PID_CART = (0, 0, 0)
# PRESET_PID_CART = (-0.924861051852458, 0.03002569629632385, -0.2994526736003437)
# PRESET_PID_CART = (-0.924861051852458, 0.03002569629632385, -0.3848792315820444)

PRESET_PID_POLE = (0, 0, 0)
PRESET_PID_POLE = (-1.8394291134013734, 0.20138629211940734, -5.200392703676353)
# PRESET_PID_POLE = (-4.512285277021222, 3.7468386916186502, 7.743010122805896)


env = gym.make('CartPole-v1')
logger = Controllers.Logger()

pole_agent = Controllers.PID_Learning_Controller(PRESET_PID_POLE)
cart_agent = Controllers.PID_Learning_Controller(PRESET_PID_CART)
# agent = cart_agent
# agent.name = 'CART'
agent = pole_agent
agent.name = 'POLE'
sum_reward = 0


def action_space(output):
    if output > 0:
        action = 1
    else:
        action = 0
    return action


for i_episode in range(Settings.EPISODES):
    observation = env.reset()
    for time_steps in range(Settings.TIME_STEPS):
        if (i_episode + 1) % Settings.EPISODE_SHOW == 0:
            env.render()
        output = 0
        output += pole_agent.get_output(observation[2], 0.0)
        # output += cart_agent.get_output(observation[0], -0.50)
        action = action_space(output)
        observation, reward, done, info = env.step(action)
        # reward -= (observation[0] - 0.50) ** 2 * 10
        sum_reward += reward
        if done:
            if (i_episode + 1) % Settings.EPISODE_PRINT == 0 or (i_episode + 1) % Settings.EPISODE_SHOW == 0:
                print("Episode {} finished after {} timesteps".format(i_episode + 1, time_steps + 1))
            break
    else:
        if (i_episode + 1) % Settings.EPISODE_PRINT == 0 or (i_episode + 1) % Settings.EPISODE_SHOW == 0:
            print("Episode {} finished after {} timesteps".format(i_episode + 1, Settings.TIME_STEPS))

    agent.reward(sum_reward)
    logger.monitor(sum_reward)
    sum_reward = 0
    if (i_episode + 1) % Settings.EPISODE_LEARN == 0:
        logger.process(i_episode + 1, Settings.EPSILON, Settings.MULTIPLIER_EPSILON)
        agent.reflect()
        agent.explore()

    if Settings.MULTIPLIER_EPSILON > 1.0:
        Settings.MULTIPLIER_EPSILON *= Settings.EPSILON_DECAY
    if Settings.EPSILON > Settings.EPSILON_CAP:
        Settings.EPSILON *= Settings.EPSILON_DECAY

    if (i_episode + 1) % Settings.EPISODE_SHOW == 0:
        log = logger.get_log()
        log += f'PRESET_PID_{agent.name} = {agent.get_string()}' + '\n'
        print(log)

env.close()
