## OVERVIEW
Shared utilities providing custom SQLAlchemy wrapper with transaction management and standardized HTTP response helpers.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Transaction management | pkg/sqlalchemy/sqlalchemy.py | auto_commit() context manager |
| Response helpers | pkg/response/response.py | 8 helper functions + Response dataclass |
| HTTP codes | pkg/response/http_code.py | HttpCode enum (6 statuses) |

## CONVENTIONS
- **Transaction Safety**: Always use `auto_commit()` context manager for DB operations
- **Response Format**: All responses use Response dataclass with code/message/data structure
- **HTTP Codes**: String-based HttpCode enum (not numeric) for consistent status handling
- **Default Values**: Response helpers accept None/empty, defaulting to empty data {}
- **Validation Errors**: validate_error_json extracts first error message from WTForms dict

## ANTI-PATTERNS (THIS PROJECT)
- **Custom Wrapper**: SQLAlchemy wrapper duplicates Flask-SQLAlchemy functionality (adds maintenance overhead)
- **String Status Codes**: HttpCode uses strings instead of standard HTTP numeric codes (non-standard)
- **Manual JSON Wrapping**: Custom response helpers vs Flask's native jsonify pattern
- **Missing 2XX Status**: All responses return HTTP 200, status in JSON body (not RESTful)
