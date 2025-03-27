from pydantic import BaseModel
from ResearchState import State
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_ollama import ChatOllama
class Reflection(BaseModel):
    reflection : str
    critique : str

model = ChatOllama(model='atlas',temperature=0,format=Reflection.model_json_schema(),num_gpu=1,num_thread=2)
def ReflectAgent(state:State,socket):
    mess = [
    SystemMessage(
        content=(
            f"You are an expert researcher in the field of {state['prompt']}. "
            "Your task is to critically reflect on and analyze the summary and hypothesis provided by the user. "
            "Provide constructive insights, identify potential gaps, and suggest improvements."
        )
    ),
    HumanMessage(
        content=(
            f"**Hypothesis:** {state['hypothesis']}\n"
            f"**Summary:** {state['summary']}\n"
            "Please provide a detailed critique."
        )
    )
    ]

    socket.emit("r",{'event' : 'reflect','label' : 'Reflecting the output generated','content' : ''})
    socket.sleep(0) 
    response = Reflection.model_validate_json(model.invoke(mess).content)
    state['reflection'] = response.reflection
    state['critique'] = response.critique
    socket.emit("r",{'event' : 'reflect','label' : 'Reflection ','content' : response.reflection})
    socket.sleep(0) 
    socket.emit("r",{'event' : 'reflect','label' : 'critique','content' : response.critique})
    socket.sleep(0) 
    return state



