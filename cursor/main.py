from .graph import create_chat_graph
import speech_recognition as sr
from langgraph.checkpoint.mongodb import MongoDBSaver
from dotenv import load_dotenv
# import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()

openai = AsyncOpenAI()

MONGODB_URI = "mongodb://localhost:27017"
config = {"configurable": {"thread_id": "1"}}

def main():
  with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
    graph = create_chat_graph(checkpointer=checkpointer)
    r = sr.Recognizer()
    with sr.Microphone() as source:
      r.adjust_for_ambient_noise(source)
      r.pause_threshold = 5
      print("Please say something:")
      audio = r.listen(source)
      print("Recognizing...")
      stt = r.recognize_google(audio)
      print("You Said: ",stt)
      for event in graph.stream({"messages": [{"role": "user", "content": stt}]}, config, stream_mode="values"):
        if "messages" in event:
          event["messages"][-1].pretty_print()
      
# main()

async def speak(text: str):
  async with openai.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="coral",
    input=text,
    instructions="Speak in a cheerful and positive tone.",
    response_format="pcm",
  ) as response:
    await LocalAudioPlayer().play(response)

# if __name__ == "__main__":
#   asyncio.run(speak(text="Today is a wonderful day to build something people love!"))