# PROJECT KNOWLEDGE BASE

**Generated:** 2026-01-13 19:19:01
**Commit:** 06832bf
**Branch:** main

## OVERVIEW
Flask-based LLM operations platform with PostgreSQL, implementing clean layered architecture using dependency injection. Integrates OpenAI API for chat completions and provides RESTful API for app management.

## STRUCTURE
```
./
├── app/http/           # Application entry point with DI setup
├── config/             # Environment-based configuration
├── internal/           # Core business logic (layered architecture)
├── pkg/                # Shared utilities (SQLAlchemy wrapper, responses)
├── test/               # Pytest test suite
└── study/              # LangChain learning materials
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Entry point | app/http/app.py | Flask app factory with Injector DI |
| API routes | internal/router/router.py | Blueprint with all endpoints |
| Business logic | internal/service/ | CRUD operations with auto_commit |
| Request handling | internal/handler/ | HTTP controllers + OpenAI integration |
| Database models | internal/model/ | SQLAlchemy ORM with UUID PKs |
| Validation | internal/schema/ | WTForms request validation |
| Configuration | config/config.py | Environment-based config loader |
| DB migrations | internal/migration/ | Alembic migration files |
| Custom exceptions | internal/exception/ | Hierarchical exception system |

## CODE MAP
| Symbol | Type | Location | Refs | Role |
|--------|------|----------|------|------|
| Http | Class | internal/server/http.py | 1 | Flask app wrapper with error handling |
| Router | Class | internal/router/router.py | 1 | Blueprint route registration |
| AppHandler | Class | internal/handler/app_handler.py | 1 | HTTP request controllers |
| AppService | Class | internal/service/app_service.py | 1 | Business logic layer |
| App | Model | internal/model/app.py | 1 | SQLAlchemy ORM model |
| SQLAlchemy | Class | pkg/sqlalchemy/sqlalchemy.py | 2 | Custom wrapper with auto_commit |
| Response | Dataclass | pkg/response/response.py | 3 | Standardized JSON responses |
| Config | Class | config/config.py | 1 | Environment configuration |

## CONVENTIONS
- **Dependency Injection**: All services use `@inject` + `@dataclass` for DI
- **Database**: UUID primary keys, datetime tracking (created_at, updated_at)
- **Validation**: WTForms with explicit error messages
- **Responses**: Unified Response dataclass with HttpCode enum
- **Transactions**: Custom `auto_commit()` context manager for DB operations
- **Exceptions**: Custom hierarchy with automatic JSON serialization
- **Type Hints**: Minimal usage, focused on config/response/exception

## ANTI-PATTERNS (THIS PROJECT)
- **Entry Point Location**: `app/http/app.py` is non-standard (should be root level)
- **Mixed Language**: .gitignore uses Chinese comments (should be English)
- **Over-engineering**: injector DI adds complexity for typical Flask apps
- **Custom SQLAlchemy**: Wrapper may add maintenance overhead vs native Flask-SQLAlchemy
- **Empty Directories**: middleware/, core/, schedule/, task/ are planned but unimplemented

## UNIQUE STYLES
- **Enterprise Java-style**: internal/ directory structure with granular separation
- **Auto-commit Pattern**: Custom SQLAlchemy wrapper with automatic commit/rollback
- **Response Utilities**: Centralized JSON response helpers instead of Flask jsonify
- **Moonshot AI Integration**: Uses Chinese AI API (kimi-k2-turbo-preview model)
- **Study Directory**: Contains LangChain learning materials in production codebase

## COMMANDS
```bash
# Run application
python -m app.http.app
# or
flask --app app.http.app run

# Database migrations
flask --app app.http.app db init
flask --app app.http.app db migrate -m "message"
flask --app app.http.app db upgrade

# Run tests
pytest -v -s

# Setup database (Docker)
docker run -d --name postgres-llmops -e POSTGRES_USER=root -e POSTGRES_PASSWORD=123456 -e POSTGRES_DB=llmops -p 5432:5432 postgres:16
```

## NOTES
- Requires PostgreSQL database running on localhost:5432
- OpenAI API key needed for chat completion (Moonshot AI)
- CSRF disabled in development (WTF_CSRF_ENABLED=False)
- SQLAlchemy query echo enabled in development
- Test coverage is minimal (only 1 test file)
- Migration files exist for app table with status column