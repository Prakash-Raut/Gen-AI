import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
from langchain.schema import SystemMessage

@tool("run_command", description="Run a command line prompt on the user's machine")
def run_command(cmd: str):
  """ Takes a command line prompt and executes it on the user's machine and returns the output 
  Example: run_command("ls") where ls is the command to list the files in the current directory.
  """
  result = os.system(command=cmd)
  return result

llm = init_chat_model(model_provider="openai", model="gpt-4.1")

tools = [run_command]

llm_with_tools = llm.bind_tools(tools=tools)

class State(TypedDict):
  messages: Annotated[list, add_messages]
  


def chatbot(state: State):
  system_prompt = SystemMessage(
    content="""
    You are an AI Coding Assistant who takes input from the user and based on 
    available tools choose the correct tool to execute commands on the user's machine.
    
    Always make sure to keep your generated codes and files in the chat_gpt/ folder.
    You can create one if it does not exist.
    """
  )
  message = llm_with_tools.invoke([system_prompt] + state["messages"])
  assert len(message.tool_calls) <= 1
  return {"messages": [message]}


tool_node = ToolNode(tools=tools)

graph_builder = StateGraph(State)

graph_builder.add_node(chatbot, "chatbot")
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges("chatbot", tools_condition)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


# With Memory
def create_chat_graph(checkpointer):
  return graph_builder.compile(checkpointer=checkpointer)
