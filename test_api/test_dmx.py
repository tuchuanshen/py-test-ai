from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="sk-my-local-key-12345",
    temperature=0.7,
    max_tokens=1000
)

#持久记忆对话
def memory_talk():
    # Define the function that calls the model
    def call_model(state: MessagesState):
        print(state["messages"])
        response = llm.invoke(state["messages"])
        print(response)
        return {"messages": response}

    # Define a new graph
    workflow = StateGraph(state_schema=MessagesState)
    # Define the (single) node in the graph
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    # Add memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": "abc123"}}


    while True:
        query = input("请输入：")
        input_messages = [HumanMessage(query)]
        output = app.invoke({"messages": input_messages}, config)
        output["messages"][-1].pretty_print()  # output contains all messages in state


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    current_prompt: str

def prompt_talk():
    test_prompt = """
    你是一个专职诗词章的助手，我给你任意题材，你都需要写出一首诗作答，不需要回答其他内容。
    例如：春江花月夜
    回答：春江潮水连海平，海上明月共潮生。
        滟滟随波千万里，何处春江无月明。
        江流宛转绕芳甸，月照花林皆似霰。
        空里流霜不觉飞，汀上白沙看不见。
        江天一色无纤尘，皎皎空中孤月轮。
        江畔何人初见月？江月何年初照人？
        人生代代无穷已，江月年年望相似。
        不知江月待何人，但见长江送流水。
        白云一片去悠悠，青枫浦上不胜愁。
        谁家今夜扁舟子？何处相思明月楼？
        可怜楼上月裴回，应照离人妆镜台。
        玉户帘中卷不去，捣衣砧上拂还来。
        此时相望不相闻，愿逐月华流照君。
        鸿雁长飞光不度，鱼龙潜跃水成文。
        昨夜闲潭梦落花，可怜春半不还家。
        江水流春去欲尽，江潭落月复西斜。
        斜月沉沉藏海雾，碣石潇湘无限路。
        不知乘月几人归，落月摇情满江树。
    """

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "{current_prompt}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    #workflow = StateGraph(state_schema=MessagesState)
    workflow = StateGraph(state_schema=State)
    def call_model(state: State):
        prompt = prompt_template.invoke(state)
        response = llm.invoke(prompt)
        return {"messages": response}


    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    config = {"configurable": {"thread_id": "1"}}
    p_time = 0
    while True:
        query = input("\n请输入：")
        input_messages = [HumanMessage(query)]
        if p_time == 0:
            p_time += 1
            output = app.invoke({"messages": input_messages, "current_prompt":test_prompt}, config)
        else:
            output = app.invoke({"messages": input_messages}, config)
        output["messages"][-1].pretty_print()  # output contains all messages in state



if __name__ == "__main__":
    prompt_talk()