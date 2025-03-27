# hypothesis_generator.py
from ResearchState import State
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage


class HypothesisStruct(BaseModel):
    hypothesis: str
    topics : list[str]



from langchain_ollama import ChatOllama
model = ChatOllama(model='atlas',temperature=0,format=HypothesisStruct.model_json_schema(),num_gpu=1,num_thread=2)
print("model started")


def generate_hypothesis(state: State,socket) -> str:
    prompt = state["prompt"]
    mess = [
        SystemMessage(content=f"You are a top researcher in {prompt}.  Generate a **single hypothesis** strictly related to {prompt}.  Also, provide **5 relevant search keywords** that include the topic word '{prompt}'."),
        HumanMessage(content=prompt)
    ]
    response = model.invoke(mess).content
    hypothesis = HypothesisStruct.model_validate_json(response)
    print(f"Generated a initial hypothesis")
    state['hypothesis'] = hypothesis.hypothesis
    state['topics'] = hypothesis.topics
    print(state)
    
    return state
