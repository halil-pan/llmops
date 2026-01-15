import dotenv
import os

from datetime import datetime

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是 OpenAI 开发的聊天机器人，请回答用户的问题，现在的时间是{now}"),
    ("human", "{query}"),
]).partial(now=datetime.now())

llm = ChatOpenAI(
    model="kimi-k2-0905-preview",
    api_key=os.getenv("OPEN_API_KEY"),
    base_url=os.getenv("OPEN_API_BASE"),
)

parser = StrOutputParser()

content = parser.invoke(llm.invoke(prompt.invoke({"query": "你好，你是？"})))

print(content)