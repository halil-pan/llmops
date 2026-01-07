import uuid
from dataclasses import dataclass
from pkg.sqlalchemy import SQLAlchemy
from injector import inject
from internal.model import App

@inject
@dataclass
class AppService:
    db: SQLAlchemy

    def create_app(self) -> App:
        with self.db.auto_commit():
            app = App(
                name="bot",
                account_id=uuid.uuid4(),
                icon="",
                description="A simple bot",
            )
            self.db.session.add(app)
        return app

    def get_app(self, id: uuid.UUID) -> App:
        app = self.db.session.query(App).get(id)
        return app

    def update_app(self, id: uuid.UUID):
        with self.db.auto_commit():
            app = self.get_app(id)
            app.name = "bot1"
        return app

    def delete_app(self, id: uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(id)
            self.db.session.delete(app)
        return app