from agent_torch.core.llm.archetype import Archetype
from agent_torch.core.llm.behavior import Behavior
import random
import pandas as pd
from agent_torch.populations import NYC

#llama api dependency
#initialize llm instance w/ langchain

#defining archetypes
archetype_supplier = Archetype(n_arch=2000)
archetype_manager = Archetype(n_arch=4500)
archetype_customer = Archetype(n_arch=23000)

#prompt template
#attributes from data: gender, age, race, community composition.
#user-defined attributes: number of flights, number of stops per flight
seller_prompt_template = "You are a supplier in Canada. You sell produce to grocery stores across Canada, including those in Nunavut. You need to make a decision as to how you will price your produce to these stores in Nunavut, taking into consideration factors like labour costs, demand of your produce, cost of transport/delivery, and supply and demand. Currently, every week, there are {num_planes} making shipments to all Nunavut grocery stores per week, each making {num_stops}. Keep in mind that if you price your produce too high, fewer grocery stores will be willing to buy, but if you price it too low, you will not make a profit. With all of this in mind, what price will you charge per unit of produce? Output a dollar amount only."
buyer_prompt_template = "You are a store manager in Nunuvut. Your age is {age}, your gender is {gender}, and your race is {race}. You live in a community in Nunavut specified by {area} and your grocery store serves the entire community of {population}. You need to decide how much produce to buy, taking factors like current inventory, current demand, costs of shipping, and needs of the community into account. Currently, every week, there are {num_planes} making shipments to all Nunavut grocery stores per week, each making {num_stops}. The price that suppliers are charging is {charged_price}. Also, you may not know when the next shipment is available since your community is remote with limited infrastructure. With all of this in mind, how many units of produce will you buy? Please state one non-negative integer only."

# Create a behavior model
# You have options to pass any of the above created llm objects to the behavior class
# Specify the region for which the behavior is to be sampled. This should be the name of any of the regions available in the populations folder.
selling_behaviour = Behavior(
    archetype=archetype_supplier.llm(llm=llm_dspy, user_prompt=seller_prompt_template, num_agents=2000)
)

buying_behaviour = Behavior(
    archetype=archetype_customer.llm(llm=llm_dspy, user_prompt=buyer_prompt_template, num_agents=4500)
)

household = pd.read_pickle("nunavut_household_data.pkl")
population = pd.read_pickle("nunavut_population__data.pkl")

#charged_price = #answer to first prompt

def call_model(num_planes, num_stops, charged_price):
    random_int = random.randint(1, 450)
    kwargs = {
        'age': population.iloc[random_int]['age'],
        'gender': population.iloc[random_int]['gender'],
        'race': population.iloc[random_int]['ethnicity'],
        'area': population.iloc[random_int]['area'],
        'population': household.iloc[random_int]['people_num'],
        'num_planes': num_planes,
        'num_stops': num_stops,
        'charged_price': charged_price,
        "device": "cuda:0",
        "current_memory_dir": "population/conversation_history/",
    }

print("Behavior model created successfully!")