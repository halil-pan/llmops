from datetime import datetime
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import AIMessage


prompt = PromptTemplate.from_template("请讲要给关于{subject}的冷笑话")
print(prompt.format(subject="程序员"))
# 请讲要给关于程序员的冷笑话

prompt_value = prompt.invoke({ "subject": "程序员" })
print(prompt_value.to_string())
# 请讲要给关于程序员的冷笑话
print(prompt_value.to_messages())
# [HumanMessage(content='请讲要给关于程序员的冷笑话')]

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个聊天机器人，请根据用户提问进行恢复，当前时间为:{now}"),
    MessagesPlaceholder("chat_history"),
    HumanMessagePromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
]).partial(now=datetime.now())
chat_prompt_value = chat_prompt.invoke({
    "chat_history": [
        ("human", "我叫小海"),
        AIMessage("你好，我是 ChatBot，有什么可以帮到您")
    ],
    "subject": "程序员",
})
print(chat_prompt_value)
# messages=[SystemMessage(content='你是一个聊天机器人，请根据用户提问进行恢复，当前时间为:2026-01-08 16:50:08.391075'), HumanMessage(content='我叫小海'), AIMessage(content='你好，我是 ChatBot，有什么可以帮到您'), HumanMessage(content='请讲一个关于程序员的冷笑话')]
print(chat_prompt_value.to_string())
# System: 你是一个聊天机器人，请根据用户提问进行恢复，当前时间为:2026-01-08 16:50:08.391075
# Human: 我叫小海
# AI: 你好，我是 ChatBot，有什么可以帮到您
# Human: 请讲一个关于程序员的冷笑话