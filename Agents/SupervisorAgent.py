import generationAgent as Gagent
import hypothsisAgent as Hagent
import proximityMetaAgent as PMagent
import RankingAgent as Ragent
import reflectionAgent as ReAgent
from ResearchState import State
from saveMD import save_to_markdown
import time



def execute(prompt:str,socket):
    print(f"Prompt received ->> {prompt}")
    
    t = time.time()
    k = State()
    k['cycles'] = 2
    k['summary'] = []
    k['prompt'] = prompt
    
    print("generating hypothesis")
    socket.emit("r",{'event' : 'hypothesis','label' : 'generating Hypothesis','content' : ''})
    socket.sleep(0) 
    k = Hagent.generate_hypothesis(k,socket=socket)
    c = k['hypothesis']
    socket.emit("r",{'event' : 'hypothesis','label' : 'Hypothesis Generated','content' : c})
    socket.sleep(0) 
    print("preparing the summary")
    while True:
        k = Gagent.generationAgent(k,socket=socket)
        print("reflecting the output")
        k = ReAgent.ReflectAgent(k,socket=socket)
        print("ranking and evaluating the reflection output")
        k = Ragent.RankAgent(k,socket=socket)
        print("checking proxmimty and provind a feedback")
        if k["cycles"] == 1:
            
            break
        else:
            k['cycles'] -=1
    k = PMagent.ProximityAgent(k,socket=socket)
    print("\n\n\n")
    print(k['research'])
    save_to_markdown(k['research'])

    print(f"time taken is ->>>   {time.time()-t}")

    
