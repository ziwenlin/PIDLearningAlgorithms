EPISODE_MULTIPLIER = 10
EPISODE_CAP = EPISODE_MULTIPLIER * 1000
EPISODE_SHOW = EPISODE_MULTIPLIER * 100
EPISODE_PRINT = EPISODE_MULTIPLIER * 10
EPISODE_PRINT_TOGGLE = False
EPISODE_RENDER = 50

TIME_STEPS = 200
EPISODE_LEARN = 20

EPSILON = 0.9
EPSILON_CAP = 0.05
EPSILON_DISCOUNT = 0.95
EPSILON_DECAY_RATE = EPSILON_DISCOUNT ** (10 / EPISODE_CAP)

MULTIPLIER_EPSILON = 10
MULTIPLIER_IMPROVE = 0.2
MULTIPLIER_RAND = 0.1


def recalculate(multiplier):
    global EPISODE_CAP, EPISODE_SHOW, EPISODE_PRINT, EPSILON_DECAY_RATE
    global EPISODE_MULTIPLIER
    EPISODE_MULTIPLIER = multiplier
    EPISODE_CAP = EPISODE_MULTIPLIER * 1000
    EPISODE_SHOW = EPISODE_MULTIPLIER * 100
    EPISODE_PRINT = EPISODE_MULTIPLIER * 10
    EPSILON_DECAY_RATE = EPSILON_DISCOUNT ** (10 / EPISODE_CAP)


def get_dict():
    return {
        'EPISODE_CAP': EPISODE_CAP,
        'EPISODE_SHOW': EPISODE_SHOW,
        'EPISODE_PRINT': EPISODE_PRINT,
        'EPISODE_PRINT_TOGGLE': EPISODE_PRINT_TOGGLE,
        'EPISODE_RENDER': EPISODE_RENDER,

        'TIME_STEPS': TIME_STEPS,
        'EPISODE_LEARN': EPISODE_LEARN,

        'EPSILON': EPSILON,
        'EPSILON_CAP': EPSILON_CAP,
        'EPSILON_DISCOUNT': EPSILON_DISCOUNT,
        # 'EPSILON_DECAY_RATE': EPSILON_DECAY_RATE,

        'MULTIPLIER_EPSILON': MULTIPLIER_EPSILON,
        'MULTIPLIER_IMPROVE': MULTIPLIER_IMPROVE,
        'MULTIPLIER_RAND': MULTIPLIER_RAND,
    }

def set_dict(info):
    for id, value in info:
        if id in ['EPISODE_MULTIPLIER','EPSILON_DECAY_RATE',]:
            continue
        globals()[id] = value

