from dataclasses import dataclass
from injector import inject
from flask import Flask, Blueprint
from internal.handler import AppHandler


@inject
@dataclass
class Router:
    app_handler: AppHandler

    def register_router(self, app: Flask):
        # blueprint 一组路由的集合
        bp = Blueprint("llmops", __name__)

        bp.add_url_rule("/ping", view_func=self.app_handler.ping)
        bp.add_url_rule('/app/completion', methods=["POST"], view_func=self.app_handler.completion)
        bp.add_url_rule('/app', methods=["POST"], view_func=self.app_handler.create_app)
        bp.add_url_rule('/app/<uuid:id>', view_func=self.app_handler.get_app)
        bp.add_url_rule('/app/<uuid:id>', methods=["POST"], view_func=self.app_handler.update_app)
        bp.add_url_rule('/app/<uuid:id>/delete', methods=["POST"], view_func=self.app_handler.delete_app)

        app.register_blueprint(bp)