import gym

from src import controllers
from src import genetics
from src import settings


class MountainCar(controllers.EnvironmentWorker):
    position = 0.6

    def get_action(self, observation: gym.core.ObsType) -> gym.core.ActType:
        output = 0
        n_point = node_point.get_output(observation, 0.0)
        n_cart = node_cart.get_output(observation, 0.0)
        position = pid_point.get_output((n_point,), self.position)
        output += pid_cart.get_output((n_cart,), position)
        # if observation[1] < 0:
        #     output = cart_agent.get_output(observation[0], 0.6)
        # elif observation[1] > 0:
        #     output = cart_agent.get_output(observation[0], -1.2)
        action = action_space(output)
        return action

    def get_reward(self, observation: gym.core.ObsType) -> float:
        reward = 0
        position, speed = observation
        if manager.name in ('PID_CART'):
            reward += abs(speed) ** 0.5
            reward -= abs(position - 0.5) ** 0.5
        elif manager.name in ('PID_POINT', 'NODE_POINT', 'NODE_CART'):
            reward += abs(speed) ** 0.2
            reward -= abs(position - 0.5) ** 0.5
        else:
            reward += abs(speed) ** 0.5
            reward -= abs(position - 0.5) ** 0.3
        return reward


def action_space(output):
    if output > 0.1:
        action = 2
    elif output < -0.1:
        action = 0
    else:
        action = 1
    return action


settings.EPISODE.CAP *= 10
settings.TIME_STEPS = 250

PID_CART = (0, 0, 0)
# PID_CART = (-1.2978, -0.0252, -0.8364)
# PID_CART = (-1.8086, -0.0327, -0.7587)
PID_POINT = (0, 0, 0)
NODE_CART = (0, 0)
NODE_POINT = (0, 0)

pid_cart: controllers.IOModel
pid_point: controllers.IOModel
node_cart: controllers.IOModel
node_point: controllers.IOModel
manager: controllers.BaseManager | \
         controllers.LearningController


def generate_improving_model():
    global manager, pid_cart, pid_point, node_cart, node_point
    pid_cart = controllers.ImprovingPIDModel('PID_CART', PID_CART)
    pid_point = controllers.ImprovingPIDModel('PID_POINT', PID_POINT)
    node_cart = controllers.ImprovingNodeModel('NODE_CART', NODE_CART)
    node_point = controllers.ImprovingNodeModel('NODE_POINT', NODE_POINT)
    manager = controllers.ImprovingControllerManager()
    manager.add_controller(pid_cart)
    manager.add_controller(pid_point)
    manager.add_controller(node_cart)
    manager.add_controller(node_point)
    pid_cart = pid_cart.model
    pid_point = pid_point.model
    node_cart = node_cart.model
    node_point = node_point.model


def generate_genetic_model():
    global manager, pid_cart, pid_point, node_cart, node_point
    pid_cart = controllers.PIDModel(PID_CART)
    pid_point = controllers.PIDModel(PID_POINT)
    node_cart = controllers.NodeModel(NODE_CART)
    node_point = controllers.NodeModel(NODE_POINT)
    manager = genetics.GeneticEvolutionController()
    manager.add_controller(pid_cart)
    manager.add_controller(pid_point)
    manager.add_controller(node_cart)
    manager.add_controller(node_point)
    manager.resize_genetic_population(20)


def main():
    generate_genetic_model()
    env = gym.make('MountainCar-v0')
    environment = controllers.EnvironmentManager(env, manager, MountainCar(env))

    environment.run()
    for i in range(manager.get_size()):
        manager.select_controller(i)
        print(manager.name, '=', manager.get_string())


if __name__ == '__main__':
    main()
