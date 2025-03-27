from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage,SystemMessage
from ResearchState import State
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash',temperature=0,api_key=os.getenv("GEMINI_API2"))

def ProximityAgent(state:State,socket):
    system_message_content = """
    You are a research analysis agent. Your task is to generate a comprehensive research report based on the provided summaries, updated hypotheses, and user prompt.
    Analyze the relationships between the summaries and hypotheses, identify key findings, potential connections, and any conflicting results.
    Provide a detailed overview and suggest potential future research directions.
    """

    human_message_content = f" User Prompt: {state['prompt']}. hypothesis : {state['hypothesis']}. Summaries:{'summary ->'.join(state['summary'])}"

    socket.emit("r",{'event' : 'review','label' : 'finding the best results from previous data','content' : '',"type" : "experiment",})
    socket.sleep(0) 

    mess = [
        SystemMessage(system_message_content),
        HumanMessage(human_message_content)
    ]
    socket.emit("r",{'event' : 'review','label' : 'preparing the final output','content' : '','type' : 'document'})
    socket.sleep(0) 
    k = model.invoke(mess).content
    state['research'] = k
    socket.emit("r",{'event' : 'review','label' : 'final Result','content' : k,'type' : 'completion'})
    socket.sleep(0) 
    return state