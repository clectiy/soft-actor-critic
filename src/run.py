from agent import AntAgent
from sac import SAC

num_iterations = 4
num_steps = 1000

# Initialise policy
config = dict()
config['epochs'] = 3
config['learning_rate'] = 0.001
config['target_update'] = 10
config['gamma'] = 0.9
config['model_name'] = 'experiments'
config['seed'] = 42 
config['log_step'] = 1
config['train_batch_size'] = 128
config['valid_batch_size'] = 128
config['optimizer'] = 'sgd'
config['initializer'] = 'xavier'
config['logs_path'] = '../data'
config['split'] = 0.8
model = SAC(config)

# Initialise agent, environment and policy
render = True
agent = AntAgent(render=render, model=None)

# Initialize replay memory


# For iteration:
for iteration in range(num_iterations):

    done=True
    transition = dict()
    # For each step:
    for step in range(num_steps):

        if done is True:

            # If episode is completed add it to replay memory
            if step != 0:
                agent.buffer.add_episode(episode_id)
                print ("episode: ", episode_id)

            # Initialize episode
            transition['current_observation'] = agent.reset_environment()
            episode_id = agent.buffer.create_episode()
            done = False
            transition = dict()

        transition['current_observation'] = agent.current_observation

        # sample an action from policy \pi_{\phi}(a_t | s_t)
        transition['action'] = agent.get_action(transition['current_observation'])

        # sample a next state from the environment based on transition probability
        transition['next_observation'], transition['reward'], done = agent.get_transitions(transition['action'])

        # Add this transition to the replay buffer
        agent.buffer.add_sample(episode_id, transition)

    agent.model = model
    # Train the SAC model with transitions in replay buffer.
    agent.learn()
