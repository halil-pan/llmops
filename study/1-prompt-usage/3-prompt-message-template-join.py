from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

system_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是 OpenAI 开发的聊天机器人，请根据用户的提问进行回复，我叫{username}"),
])
human_chat_prompt = ChatPromptTemplate.from_messages([
    ("human", "{query}")
])

chat_prompt = system_chat_prompt + human_chat_prompt

print(chat_prompt)
# input_variables=['query', 'username'] input_types={} partial_variables={} messages=[SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=['username'], input_types={}, partial_variables={}, template='你是 OpenAI 开发的聊天机器人，请根据用户的提问进行回复，我叫{username}'), additional_kwargs={}), HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['query'], input_types={}, partial_variables={}, template='{query}'), additional_kwargs={})]

print(chat_prompt.invoke({
    "username": "小海",
    "query": "你好，你是？"
}))
# messages=[SystemMessage(content='你是 OpenAI 开发的聊天机器人，请根据用户的提问进行回复，我叫小海', additional_kwargs={}, response_metadata={}), HumanMessage(content='你好，你是？', additional_kwargs={}, response_metadata={})]