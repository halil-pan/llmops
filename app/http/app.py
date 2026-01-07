import dotenv
from pkg.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from injector import Injector, Module, Binder

from internal.router import Router
from internal.server import Http
from config import Config
from internal.extension.database_extension import db
from internal.extension.migrate_extension import migrate

dotenv.load_dotenv()
conf = Config()

class ExtensionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, to=db)
        binder.bind(Migrate, to=migrate)

injector = Injector([ExtensionModule])

app = Http(__name__, conf=conf, db=injector.get(SQLAlchemy), migrate=injector.get(Migrate), router=injector.get(Router))

if __name__ == "__main__":
    app.run(debug=True)