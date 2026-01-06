import uuid
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from injector import inject
from internal.model import App

@inject
@dataclass
class AppService:
    db: SQLAlchemy

    def create_app(self) -> App:
        app = App(
            name="bot",
            account_id=uuid.uuid4(),
            icon="",
            description="A simple bot",
        )
        self.db.session.add(app)
        self.db.session.commit()
        return app
