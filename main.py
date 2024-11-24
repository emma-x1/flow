import argparse
from tqdm import trange
from simulator import get_registry, get_runner

from agent_torch.core.helpers import read_config
from agent_torch.core.registry import Registry

config = read_config('config-map.yaml')
metadata = config.get('simulation_metadata')
num_episodes = metadata.get('num_episodes')
num_steps_per_episode = metadata.get('num_steps_per_episode')
num_substeps_per_step = metadata.get('num_substeps_per_step')

registry = Registry()
registry.register(read_from_file, 'read_from_file', 'initialization')
registry.register(grid_network, 'grid', key='network')

runner = get_runner(config, registry)
runner.run()