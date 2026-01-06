import os

from flask import request
from openai import OpenAI
from internal.schema import CompletionReq


class AppHandler:
    def ping(self):
        return {"ping": "pong"}

    def completion(self):
        """ ai chat """
        req = CompletionReq()
        if not req.validate():
            return req.errors

        # 提取接口获取输入
        query = request.json.get("query")

        # 构建 openai 客户端发起请求
        client = OpenAI(
            api_key=os.getenv("OPEN_API_KEY"),
            base_url=os.getenv("OPEN_API_BASE"),
        )

        # 将相应传给前端
        completion = client.chat.completions.create(
            model="kimi-k2-turbo-preview",
            messages=[
                {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
                {"role": "user","content": query}
            ],
            temperature=0.6,
        )

        content = completion.choices[0].message.content
        return {"content": content}
