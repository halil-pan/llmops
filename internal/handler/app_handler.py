import os
import uuid

from flask import request
from injector import inject
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
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

        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个聊天机器人，请根据用户提问进行回复"),
            HumanMessagePromptTemplate.from_template("{query}")
        ])

        llm = ChatOpenAI(
            model="kimi-k2-0905-preview",
            api_key=os.getenv("OPEN_API_KEY"),
            base_url=os.getenv("OPEN_API_BASE"),
        )

        parser = StrOutputParser()

        content = parser.invoke(llm.invoke(prompt.invoke({"query": req.query.data})))

        return success_json({"content": content})

    def ping(self):
        raise FailException("数据未找到")
        # return {"ping": "pong"}