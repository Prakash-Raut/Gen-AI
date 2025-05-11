# from .graph import graph
from .graph import create_chat_graph
from langgraph.checkpoint.mongodb import MongoDBSaver
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = "mongodb://localhost:27017"
config = {"configurable": {"thread_id": "1"}}

def stream_graph_updates(user_input: str, graph_with_mongo):
  for event in graph_with_mongo.stream({"messages": [{"role": "user", "content": user_input}]}, config, stream_mode="values"):
    if "messages" in event:
      event["messages"][-1].pretty_print()

def init():
  print("Welcome to LangGraph!")
  with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
    graph_with_mongo = create_chat_graph(checkpointer=checkpointer)
    while True:
      try:
        user_input = input("> ")
        if user_input.lower() in ["exit", "quit", "q"]:
          print("GoodBye!")
          break
        stream_graph_updates(user_input, graph_with_mongo)
      except:
        user_input = "What do you know about LangGraph?"
        stream_graph_updates(user_input, graph_with_mongo)
        break
    
init()