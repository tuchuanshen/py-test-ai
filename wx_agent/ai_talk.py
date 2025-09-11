from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import END, StateGraph
from typing import Annotated, Sequence, TypedDict
import operator

# 初始化语言模型
llm = ChatOpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="sk-my-local-key-12345",
    temperature=0.7,
    max_tokens=1000
)

# 定义工具
@tool
def calculator(expression: str) -> str:
    """执行简单的数学计算"""
    try:
        # 安全计算表达式
        allowed_chars = set('0123456789+-*/(). ')
        cleaned_expression = ''.join(c for c in expression if c in allowed_chars)
        result = eval(cleaned_expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算出错: {str(e)}"

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    # 模拟天气查询
    return f"{city}的天气是晴天，温度25°C，湿度60%"

# 工具列表
tools = [calculator, get_weather]
llm_with_tools = llm.bind_tools(tools)

# 定义图的状态
class AgentState(MessagesState):
    pass

# 定义节点函数
def call_model(state: AgentState):
    """调用语言模型"""
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    """决定是否继续执行工具"""
    messages = state["messages"]
    last_message = messages[-1]
    if hasattr(last_message, 'tool_calls') and len(last_message.tool_calls) > 0:
        return "tools"
    return END

# 创建图
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# 添加边
workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END,
    },
)
workflow.add_edge("tools", "agent")

# 添加记忆
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

def smart_qa():
    """智能问答主函数"""
    config = {"configurable": {"thread_id": "smart_qa_thread"}}
    
    print("智能问答系统已启动，支持以下功能:")
    print("1. 基础问答")
    print("2. 数学计算 (例如: 123+456)")
    print("3. 天气查询 (例如: 北京天气)")
    print("输入 '退出' 结束对话\n")
    
    while True:
        query = input("用户: ")
        if query.lower() == '退出':
            print("对话结束")
            break
            
        input_message = HumanMessage(content=query)
        result = app.invoke({"messages": [input_message]}, config)
        response = result["messages"][-1].content
        print(f"助手: {response}\n")

if __name__ == "__main__":
    smart_qa()