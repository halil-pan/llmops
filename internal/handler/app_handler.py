import os
import uuid

from flask import request
from injector import inject
from openai import OpenAI
from dataclasses import dataclass

from internal.exception import FailException
from internal.schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message


@inject
@dataclass
class AppHandler:
    app_service: AppService

    def create_app(self):
        app = self.app_service.create_app()
        return success_message(f"应用已经成功创建，id 为 {app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        return success_message(f"应用已经成功获取，名字是{app.name}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"应用已经成功修改，名字是{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"应用已经成功删除，id 为{app.id}")

    def completion(self):
        """ ai chat """
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

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

        return success_json({"content": content})

    def ping(self):
        raise FailException("数据未找到")
        # return {"ping": "pong"}