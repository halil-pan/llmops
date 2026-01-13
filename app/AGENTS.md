# APP DIRECTORY

## OVERVIEW
Flask application factory using Injector for dependency injection setup and extension binding.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| DI Configuration | app/http/app.py | ExtensionModule binds SQLAlchemy/Migrate |
| App Initialization | app/http/app.py | injector.get() resolves dependencies for Http instance |
| Extension Instances | internal/extension/ | Global db/migrate singleton instances |

## CONVENTIONS
- **DI Module Pattern**: Uses `ExtensionModule` class with `configure()` method for dependency binding
- **Global Extensions**: SQLAlchemy/Migrate instantiated globally in `internal/extension/` then bound to injector
- **Environment Loading**: dotenv.load_dotenv() called before Config() initialization
- **Injector Pattern**: Centralized injector instance resolves all dependencies via `.get()` method

## ANTI-PATTERNS
- **Non-standard location**: Entry point nested in `app/http/app.py` instead of project root (`app.py`)
- **Missing __init__**: Both `app/` and `app/http/` have empty `__init__.py` files (unnecessary namespace packaging)
- **Mixed DI styles**: Uses Module pattern here, but `@inject` decorators in internal/services/
