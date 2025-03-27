from langchain_core.messages import HumanMessage,SystemMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from ResearchState import State
class Rank(BaseModel):
    hypothesis_rank: int
    hypothesis_explanation: str
    summary_rank: int
    summary_explanation: str
    reflection_rank: int
    reflection_explanation: str
    critique_rank: int
    critique_explanation: str

class HypothesisStruct(BaseModel):
    hypothesis: str
    topics : list[str]
model = ChatOllama(model="atlas",temperature=0,format=Rank.model_json_schema(),num_gpu=1,num_thread=2)
model1 = ChatOllama(model="atlas",temperature=0,format=HypothesisStruct.model_json_schema(),num_gpu=1,num_thread=2)

def RankAgent(state:State,socket):
    socket.emit("r",{'event' : 'rank','label' : 'Ranking the data ','content' : ''})
    socket.sleep(0)

    mess = [
    SystemMessage(
        "You are an expert evaluator. You will be provided with a hypothesis, a summary, a reflection, and a critique. Your task is to rank each of these elements based on their overall quality and impact, using a scale of 1 to 10, where 1 is the lowest and 10 is the highest. Provide the rank for each element, and a very brief explanation for each rank."
    ),
    HumanMessage(
        f"""
        Hypothesis: {state['hypothesis']}

        Summary: {state['summary']}

        Reflection: {state['reflection']}

        Critique: {state['critique']}

        Please provide the ranks and explanations in the following format:

        Hypothesis Rank: [Rank] - [Explanation]
        Summary Rank: [Rank] - [Explanation]
        Reflection Rank: [Rank] - [Explanation]
        Critique Rank: [Rank] - [Explanation]
        """
    )]

    k = Rank.model_validate_json(model.invoke(mess).content)

    ranks = f"**Hypothesis Rank : {k.hypothesis_rank}** \n **Summary Rank : {k.summary_rank}**"
    socket.emit("r",{'event' : 'rank','label' : 'Providing Ranks to output ','content' : ranks})
    socket.sleep(0)
    mess = [
        SystemMessage(
            "You are an expert researcher. You will be provided with an original hypothesis, and ranking data of the original hypothesis, summary, reflection, and critique. Your task is to use the provided ranks and explanations to refine the original hypothesis, making it more robust and accurate. If the hypothesis rank is high, still consider the critique to make it better. If the hypothesis rank is low, use the other ranks and explanations to create a new, refined hypothesis. and also provide 3 search queries related to topic.the search query should represent that domain also"
        ),
        HumanMessage(
            f"""
        Original Hypothesis: {state['hypothesis']}

        Hypothesis Rank: {k.hypothesis_rank} - {k.hypothesis_explanation}
        Summary Rank: {k.summary_rank} - {k.summary_explanation}
        Reflection Rank: {k.reflection_rank} - {k.reflection_explanation}
        Critique Rank: {k.critique_rank} - {k.critique_explanation}

        Please provide a refined hypothesis based on this information.
        """
        ),
    ]

    k = HypothesisStruct.model_validate_json(model1.invoke(mess).content)
    socket.emit("r",{'event' : 'hypothesis','label' : 'Refining Hypothesis','content' : k.hypothesis})
    socket.sleep(0) 
    state['hypothesis'] = k.hypothesis
    state['topics'] = k.topics
    return state
    