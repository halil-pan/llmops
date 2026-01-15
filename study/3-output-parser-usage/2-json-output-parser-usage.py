import dotenv
import os

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

class Joke(BaseModel):
    joke: str = Field(description="回答用户的冷笑话")
    punchline: str = Field(description="这个冷笑话的笑点")

parser = JsonOutputParser(pydantic_object=Joke)

prompt = (ChatPromptTemplate.from_template("请根据用户提问进行回答，\n{format_instructions}\n{query}")
          .partial(format_instructions=parser.get_format_instructions()))

llm = ChatOpenAI(
    model="kimi-k2-0905-preview",
    api_key=os.getenv("OPEN_API_KEY"),
    base_url=os.getenv("OPEN_API_BASE"),
)

joke = parser.invoke(llm.invoke(prompt.invoke({"query": "请讲一个关于程序员的冷笑话"})))
print(joke)
print(type(joke))
print(joke.get("punchline"))