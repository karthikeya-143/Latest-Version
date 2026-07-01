import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from langserve import add_routes
import uvicorn

_=load_dotenv(find_dotenv())

google_api_key = os.getenv("GOOGLE_API_KEY")
llmModel = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key
)
parser=StrOutputParser()
system_template="Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", "{text}"),
    ]
)
chain=prompt_template|llmModel|parser

app=FastAPI(
    title="simple translation API",
    version="1.0",
    description="A simple translation API using Langserve and Langchain",
)
add_routes(app, chain,path="/chain")

if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=8000)