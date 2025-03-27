from typing import TypedDict

class State(TypedDict):
    prompt : str
    hypothesis : str
    summary : list[str]
    cycles : int
    topics : list[str]
    reflection : str
    critique : str
    research : str