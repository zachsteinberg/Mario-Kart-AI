import retro
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import BoltzmannQPolicy
from keras.models import Model, Sequential
from keras.layers import Dense, Flatten, Input
from keras.wrappers.scikit_learn import KerasClassifier
from keras.optimizers import Adam

# Create environment
env = retro.make(game='SuperMarioKart-Snes', use_restricted_actions=retro.Actions.DISCRETE)
num_actions = env.action_space.n
state_size = env.observation_space.shape

# Define deep learning model
def build_model(state_size, num_actions):
    # create model
    model = Sequential()
    model.add(Flatten(input_shape=(1,) + state_size))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(num_actions, activation='linear'))

    print(model.summary())
    return model

# Instantiate model
model = build_model(state_size, num_actions)

# Create memory class to store agent's experiences
memory = SequentialMemory(limit=50000, window_length=1)

# Define a policy
policy = BoltzmannQPolicy()

# Create the agent
agent = DQNAgent(
    model=model, 
    nb_actions=num_actions, 
    memory=memory, 
    nb_steps_warmup=1000,
    target_model_update=1e-2, 
    policy=policy
)

agent.compile(Adam(lr=1e-3), metrics=['mae'])

'''
# Set up callbacks
def build_callbacks(env_name):
    checkpoint_weights_filename = 'dqn_' + env_name + '_weights_{step}.h5f'
    log_filename = 'dqn_{}_log.json'.format(env_name)
    callbacks = [ModelIntervalCheckpoint(checkpoint_weights_filename, interval=5000)]
    callbacks += [FileLogger(log_filename, interval=100)]
    return callbacks

# Fit model
callbacks = build_callbacks(ENV_NAME)

dqn.fit(env, nb_steps=50000,
visualize=False,
verbose=2,
callbacks=callbacks)
'''

# Fit model
agent.fit(
    env,
    nb_steps=1000,
    visualize=False,
    verbose=1
)

# Test model
agent.test(env, nb_episodes=5, visualize=True)
