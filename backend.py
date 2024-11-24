from abc import abstractmethod, ABC
import ollama
import concurrent
import dspy
import io, sys, os

class LLMBackend(ABC):
    def __init__(self):
        pass

    def initialize_llm(self):
        raise NotImplementedError

    @abstractmethod
    def prompt(self, prompt_list):
        pass

    def inspect_history(self, last_k, file_dir):
        raise NotImplementedError

# https://dspy.ai/learn/programming/language_models/?h=ollama#__tabbed_1_5

class OllamaLLM(LLMBackend):
    def __init__(self, qa, cot, model="llama3.2"):
        super().__init__()
        self.qa = qa
        self.cot = cot
        self.backend = "dspy"
        self.model = model

    def initialize_llm(self):
        self.llm = dspy.LM(
            f'ollama_chat/{self.model}', api_base='http://localhost:11434', api_key='', temperature=0.7
        )
        dspy.settings.configure(lm=self.llm)
        self.predictor = self.cot(self.qa)
        return self.predictor

    def prompt(self, prompt_list):
        agent_outputs = self.call_ollama_agent(prompt_list)
        return agent_outputs

    def call_ollama_agent(self, prompt_inputs):
        agent_outputs = []
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                agent_outputs = list(
                    executor.map(self.ollama_query_and_get_answer, prompt_inputs)
                )
        except Exception as e:
            print(e)
        return agent_outputs

    def ollama_query_and_get_answer(self, prompt_input):
        if type(prompt_input) is str:
            agent_output = self.query_agent(prompt_input, [])
        else:
            agent_output = self.query_agent(
                prompt_input["agent_query"], prompt_input["chat_history"]
            )
        return agent_output

    def query_agent(self, query, history):
        pred = self.predictor(question=query, history=history)
        print(pred)
        return pred.answer

    def inspect_history(self, last_k, file_dir):
        buffer = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = buffer
        self.llm.inspect_history(last_k)
        printed_data = buffer.getvalue()
        if file_dir is not None:
            save_path = os.path.join(file_dir, "inspect_history.md")
            with open(save_path, "w") as f:
                f.write(printed_data)
        sys.stdout = original_stdout