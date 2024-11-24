from backend import OllamaLLM
from agent_torch.core.llm.archetype import Archetype
from agent_torch.core.llm.behavior import Behavior
from agent_torch.populations import NYC
from dspy import ChainOfThought
import dspy
from backend import OllamaLLM
from population import Nunavut

# https://dspy.ai/cheatsheet/?h=basicqa#dspysignature
class CustomQA(dspy.Signature):
    """Answer questions with short factoid answers."""

    question = dspy.InputField()
    answer = dspy.OutputField(desc="Answer in the first person. You are a human that follows my prompts exactly.")

llm_ollama = OllamaLLM(qa=CustomQA, cot=ChainOfThought, model='llama3.2')
llm_ollama.initialize_llm()

archetype_supplier = Archetype(n_arch=2000)
archetype_manager = Archetype(n_arch=4500)
archetype_customer = Archetype(n_arch=23000)

seller_prompt_template = "You are a supplier in Canada. You sell bread to grocery stores across Canada, including those in Nunavut. You need to make a decision as to how you will price your bread to these stores in Nunavut, taking into consideration factors like labour costs, demand of your bread, cost of transport/delivery, and supply and demand. Currently, every week, there are {num_planes} making shipments to all Nunavut grocery stores per week, each making {num_stops}. Keep in mind that if you price your produce too high, fewer grocery stores will be willing to buy, but if you price it too low, you will not make a profit. With all of this in mind, what price will you charge per loaf of bread? Output a non-negative float only (units of dollars, but don't include the dollar sign)."
buyer_prompt_template = "You are a store manager in Nunavut. Your age is {age} and your gender is {gender}. You live in a community in Nunavut specified by {area} and your grocery store serves the entire community of {population}. You need to decide how much bread to buy, taking factors like current inventory, current demand, costs of shipping, and needs of the community into account. Currently, every week, there are {num_planes} making shipments to all Nunavut grocery stores per week, each making {num_stops}. The price that suppliers are charging is {charged_price}. Also, you may not know when the next shipment is available since your community is remote with limited infrastructure. With all of this in mind, how many loafs of bread will you buy? Only respond with one non-negative integer only."

selling_behaviour = Behavior(
    archetype=archetype_supplier.llm(llm=llm_ollama, user_prompt=seller_prompt_template),
    region=Nunavut
)

buying_behaviour = Behavior(
    archetype=archetype_customer.llm(llm=llm_ollama, user_prompt=buyer_prompt_template),
    region=Nunavut
)



# archetype = Archetype(n_arch=7)
# user_prompt_template = "Your age is {age} {gender}, unemployment rate is {unemployment_rate}, and the number of COVID cases is {covid_cases}.Current month is {month} and year is {year}. Provide only a numerical value between 0 and 1 representing your willingness to work/spend. Do not include any explanation."
# earning_behavior = Behavior(
#     archetype=archetype.llm(llm=llm_ollama, user_prompt=user_prompt_template),
#     region=NYC
# )

# print(earning_behavior)

scenario_params = {
    'num_planes': 5,
    'num_stops': 3,
    'population': 1200,
    'charged_price': 10,
    'device': 'cuda:0',
    'current_memory_dir': 'population/conversation_history/',
}

# Generate behaviors
sample_sell = selling_behaviour.sample(scenario_params)
sample_buy = buying_behaviour.sample(scenario_params)
print("Population Behaviors:")
print(sample_sell)
print(sample_buy)