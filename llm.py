from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

import os
from dotenv import load_dotenv
load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm= ChatOpenAI(
    model="gpt-4o",
)

embed_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = InMemoryVectorStore(embed_model)



if __name__ == "__main__":
    text= llm.invoke("What is the capital of France?")
    print(text)