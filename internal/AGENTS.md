# INTERNAL DIRECTORY KNOWLEDGE BASE

**Generated:** 2026-01-13 19:27:00
**Parent:** ../AGENTS.md

## OVERVIEW
Core business logic implementing strict layered architecture with dependency injection for Flask application.

## STRUCTURE
```
./internal/
├── router/           # HTTP endpoint registration (Blueprint)
├── handler/          # Presentation layer (HTTP controllers)
├── service/          # Business logic layer (CRUD operations)
├── model/            # Database models (SQLAlchemy ORM)
├── schema/           # Request validation (WTForms)
├── extension/        # Flask extensions (db, migrate)
├── exception/        # Custom exception hierarchy
├── server/           # Flask app wrapper with error handling
├── migration/        # Alembic database migrations
├── core/             # Planned (empty)
├── middleware/       # Planned (empty)
├── schedule/         # Planned (empty)
└── task/             # Planned (empty)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| API endpoints | router/router.py | Blueprint registration with url rules |
| HTTP controllers | handler/app_handler.py | Request handling + OpenAI integration |
| Business logic | service/app_service.py | CRUD with auto_commit context |
| Data models | model/app.py | SQLAlchemy ORM with constraints |
| Request validation | schema/app_schema.py | WTForms with validators |
| DB extensions | extension/*.py | Flask-SQLAlchemy, Flask-Migrate instances |
| Error handling | server/http.py | CustomException JSON serialization |
| Exception types | exception/exception.py | HttpCode-based hierarchy |

## CONVENTIONS
- **Layered Separation**: Router → Handler → Service → Model (strict no cross-layer access)
- **DI Pattern**: `@inject` decorator + `@dataclass` for constructor injection
- **Service Pattern**: All DB operations wrapped in `with db.auto_commit():` context
- **Package Exports**: Each package defines `__all__` in `__init__.py`
- **Validation**: WTForms classes in schema/ for request validation
- **Model Defaults**: Use `default=` not `server_default=` for SQLAlchemy columns

## ANTI-PATTERNS (INTERNAL)
- **Over-architecture**: 4 layers (Router→Handler→Service) for simple CRUD
- **Empty Directories**: core/, middleware/, schedule/, task/ unimplemented
- **Service Logic Leak**: OpenAI client instantiation in handler (should be service)
- **Tight Coupling**: Direct environment access (os.getenv) in handlers
- **Missing Abstractions**: No interface/protocol definitions for services/handlers
