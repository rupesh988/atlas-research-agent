from pydantic import BaseModel
from dotenv import load_dotenv
import os
os.environ["OLLAMA_FORCE_GPU"] = "1"
os.environ["OLLAMA_KEEP_LOADED"] = "1"
# from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage,SystemMessage
from ResearchState import State
from summ import get_limited_info
from langchain_community.tools import DuckDuckGoSearchResults
search = DuckDuckGoSearchResults(num_results=1,output_format='list')
import reflectionAgent as refl
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-2.0-flash',temperature=0,api_key=os.getenv("GEMINI_API1"))




def generationAgent(state: State, socket):
    print("getting links")
    
    links = []
    for i in state["topics"]:
        link = search.invoke(i)
        link = link[0]
        links.append(link["link"])

    socket.emit("r", {"event": "links", "label": "searching resources", "content": "","type" : "bookmark"})
    socket.sleep(0)   

    print("loading websites")
    j =""
    for i in links:
        j += f"**{i}** \n"
    socket.emit("r", {"event": "links", "label": "scraping websites","type" : "search", "content": j})
    socket.sleep(0)

    summaries = get_limited_info(links)

    mess = [
        SystemMessage("you are a researcher who writes comprehensive paragraphs based on hypothesis, topic, and data."),
        HumanMessage(f"prompt = {state['prompt']} . hypothesis = {state['hypothesis']} . summary : {summaries}"),
    ]

    print("summarizing the content from web data")
    k = model.invoke(mess).content
    state["summary"].append(k)

    socket.emit("r", {"event": "summary", "label": "generating summary on web data", "content": k,"type" : "note"})
    socket.sleep(0)

    print(k)
    return state

##minimise above code to execute faster





