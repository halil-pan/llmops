import os

from flask import Flask
from flask_migrate import Migrate

from config import Config
from internal.model import App
from internal.router import Router
from internal.exception import CustomException
from pkg.response import Response, json, fail_message
from pkg.sqlalchemy import SQLAlchemy


class Http(Flask):
    def __init__(self, *args, conf: Config, db: SQLAlchemy, migrate: Migrate, router: Router, **kwargs):
        super().__init__(*args, **kwargs)
        self.config.from_object(conf)
        self.register_error_handler(Exception, self._register_error_handler)
        db.init_app(self)
        migrate.init_app(self, db, "internal/migration")
        # with self.app_context():
        #     _ = App()
        #     db.create_all()
        router.register_router(self)

    def _register_error_handler(self, error: Exception):
        if isinstance(error, CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if error.data is not None else {},
            ))
        if self.debug or os.getenv("FLASK_ENV") == "development":
            raise error
        return fail_message(str(error))