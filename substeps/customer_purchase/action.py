import torch
import numpy as np
import re
import torch.nn.functional as F

from agent_torch.core.helpers import get_by_path
from agent_torch.core.substep import SubstepAction, SubstepObservation, SubstepTransition
from agent_torch.core.llm.backend import LangchainLLM
from agent_torch.core.distributions import StraightThroughBernoulli

from ...calibration.utils.data import get_data, get_labels
from ...calibration.utils.feature import Feature
from ...calibration.utils.llm import AgeGroup, SYSTEM_PROMPT, construct_user_prompt
from ...calibration.utils.misc import week_num_to_epiweek, name_to_neighborhood

@Registry.register_substep("set_prices", "observation")
class WeeklyFlights(SubstepObservation):
    def __init__(self, config, input_variables, output_variables):
        super().__init__(config, input_variables, output_variables)

    def forward(self, state):
        input_variables = self.input_variables # includes num_flights
        num_flights = state.get(self.input_variables[0])

    return { self.output_variables[0]: num_flights }

@Registry.register_substep("set_prices", "action")
class WeeklyFlights(SubstepAction):
    def __init__(self, config, input_variables, output_variables):
        super().__init__(config, input_variables, output_variables)

    def forward(self, state, observation):
        # set input prob
        input_variables = self.input_variables # includes num_flights
        num_flights = state.get(self.input_variables[0])

    return { self.output_variables[0]: num_flights }

@Registry.register_substep("set_prices", "transition")
class WeeklyFlights(SubstepTransition):
    def __init__(self, config, input_variables, output_variables):
        super().__init__(config, input_variables, output_variables)

    def forward(self, state, observation):
        # set input prob
        input_variables = self.input_variables # includes num_flights
        num_flights = state.get(self.input_variables[0])

    return { self.output_variables[0]: num_flights }

# To-do 
# make sure input has start and end airports
# action function for stopping flights


