import torch
import numpy as np
import re
import torch.nn.functional as F

from agent_torch.core.helpers import get_by_path
from agent_torch.core.substep import SubstepAction, SubstepObservation, SubstepTransition
from agent_torch.core.llm.backend import LangchainLLM
from agent_torch.core.distributions import StraightThroughBernoulli
from agent_torch.core.registry import Registry

class Registry(nn.Module):
    helpers = {
        "transition": {},
        "observation": {},
        "policy": {},
        "initialization": {},
        "network": {},
    }

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
        self.manager_llm = arguments.get("manager_llm")  # LLM instance for manager
        self.supplier_llm = arguments.get("supplier_llm")  # LLM instance for supplier

    def forward(self, state, observation):
        input_data = state.get(self.input_variables[0])  # Example: num_flights

        # Generate prices using manager and supplier LLMs
        manager_price = self.manager_llm.generate_price(input_data)
        supplier_price = self.supplier_llm.generate_price(input_data)

        # Combine or reconcile the prices (e.g., average them)
        final_price = (manager_price + supplier_price) / 2

        # Return the calculated price
        return {self.output_variables[0]: final_price}


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


