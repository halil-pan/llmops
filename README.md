# LLM 运维平台

基于 Flask 的 LLM（大语言模型）运维管理平台，支持应用管理、AI 对话等功能。

## 1. 项目概述

这是一个企业级的 LLM 运维平台，采用严格的分层架构设计和依赖注入模式，为开发者提供完整的 AI 应用管理能力。

### 核心特性

- **分层架构设计**: Router（路由层）→ Handler（控制器层）→ Service（业务逻辑层）→ Model（数据层）
- **依赖注入**: 使用 Injector 框架实现松耦合的组件管理
- **数据库**: PostgreSQL + SQLAlchemy ORM，支持 Alembic 数据库迁移
- **AI 集成**: 集成月之暗面（Moonshot AI）API，提供强大的对话补全能力
- **标准化响应**: 统一的 JSON 响应格式，便于前端集成
- **异常处理**: 完善的自定义异常体系，自动序列化为 JSON

## 2. 主要功能

### 2.1 AI 对话补全
- 集成 Moonshot AI 的 kimi-k2-turbo-preview 模型
- 支持中英文对话
- 可配置的对话参数（如 temperature）
- 标准化的对话接口

### 2.2 应用管理 (CRUD)
- **创建应用**: 自动生成 UUID，初始化应用信息
- **查询应用**: 根据 UUID 查询应用详情
- **更新应用**: 支持修改应用配置和状态
- **删除应用**: 安全删除应用记录
- 完整的时间戳记录（创建时间、更新时间）

### 2.3 开发支持
- 数据库迁移管理（Alembic）
- 统一的异常处理机制
- 请求参数验证（WTForms）
- 开发环境配置（SQL 日志、调试模式）

## 3. 技术架构

### 3.1 分层架构

项目采用严格的分层架构，各层职责清晰，互不越界：

```
┌─────────────────────────────────────────┐
│          Router Layer (路由层)          │
│      定义 HTTP 端点，分发请求           │
├─────────────────────────────────────────┤
│       Handler Layer (控制器层)          │
│   处理 HTTP 请求，调用业务逻辑          │
├─────────────────────────────────────────┤
│       Service Layer (业务逻辑层)        │
│  实现业务逻辑，数据库 CRUD 操作         │
├─────────────────────────────────────────┤
│        Model Layer (数据层)             │
│        SQLAlchemy ORM 模型              │
└─────────────────────────────────────────┘
```

### 3.2 依赖注入

使用 `injector` 库实现依赖注入，各组件通过 `@inject` 装饰器声明依赖：

```python
@inject
@dataclass
class AppHandler:
    app_service: AppService  # 自动注入依赖
```

优点：
- 降低组件耦合度
- 便于单元测试（可注入 Mock 对象）
- 代码更清晰，依赖关系一目了然

### 3.3 数据库事务管理

自定义 SQLAlchemy 包装器，提供 `auto_commit()` 上下文管理器：

```python
with self.db.auto_commit():
    app = App(name="test")
    self.db.session.add(app)
# 自动提交或回滚
```

### 3.4 响应格式

所有 API 响应遵循统一格式：

```json
{
  "code": "SUCCESS",
  "message": "操作成功",
  "data": {}
}
```

HTTP 状态码统一为 200，具体状态通过 `code` 字段表示。

## 4. 项目结构

## 🛠️ 快速开始

### 环境变量配置

创建 `.env` 文件并配置以下环境变量：

```dotenv
# ============================================
# AI 服务配置
# ============================================
OPEN_API_KEY=sk-xxx
# 月之暗面 API 密钥（必填）
# 获取地址: https://platform.moonshot.cn/console/api-keys

OPEN_API_BASE=https://api.moonshot.cn/v1
# 月之暗面 API 基础地址（可选，默认该值）

# ============================================
# Flask 配置
# ============================================
FLASK_DEBUG=1
# Flask 调试模式（1=开启，0=关闭）
# 开发环境建议开启，生产环境必须关闭

FLASK_ENV=development
# Flask 运行环境（development/production）

WTF_CSRF_ENABLED=False
# CSRF 保护开关（False=关闭，True=开启）
# 开发环境建议关闭，生产环境必须开启

# ============================================
# 数据库配置
# ============================================
SQLALCHEMY_DATABASE_URI=postgresql://root:123456@localhost:5432/llmops
# 数据库连接字符串
# 格式: postgresql://用户名:密码@主机:端口/数据库名

SQLALCHEMY_POOL_SIZE=30
# 数据库连接池大小
# 根据并发需求调整，生产环境建议 10-50

SQLALCHEMY_POOL_RECYCLE=3600
# 连接回收时间（秒）
# 防止长时间空闲连接被 PostgreSQL 关闭
# 建议设置为 PostgreSQL 的 idle_in_transaction_session_timeout 的一半

SQLALCHEMY_ECHO=True
# SQL 日志输出（True=输出，False=关闭）
# 开发环境建议开启，生产环境关闭
```

### 配置加载规则

1. 优先读取环境变量
2. 环境变量未设置时使用 `config/default_config.py` 中的默认值
3. 配置通过 `Config` 类加载到 Flask 应用

### 默认配置值

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `WTF_CSRF_ENABLED` | `False` | CSRF 保护 |
| `SQLALCHEMY_DATABASE_URI` | `""` | 数据库 URI（必须配置） |
| `SQLALCHEMY_POOL_SIZE` | `30` | 连接池大小 |
| `SQLALCHEMY_POOL_RECYCLE` | `3600` | 连接回收时间（秒） |
| `SQLALCHEMY_ECHO` | `"True"` | SQL 日志输出 |

## 7. 数据库设置

### 7.1 启动 PostgreSQL (Docker)

使用 Docker 快速启动 PostgreSQL 容器：

```bash
# 启动 PostgreSQL 容器
docker run -d \
  --name postgres-llmops \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=123456 \
  -e POSTGRES_DB=llmops \
  -v pg_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16
```

**参数说明**:
- `--name`: 容器名称
- `-e POSTGRES_USER`: 数据库用户名
- `-e POSTGRES_PASSWORD`: 数据库密码
- `-e POSTGRES_DB`: 数据库名称
- `-v pg_data:/var/lib/postgresql/data`: 数据持久化卷
- `-p 5432:5432`: 端口映射（宿主机:容器）

### 7.2 验证数据库连接

```bash
# 进入容器
docker exec -it postgres-llmops psql -U root -d llmops

# 查看数据库列表
\l

# 查看表列表
\dt

# 退出
\q
```

### 7.3 停止和删除容器

```bash
# 停止容器
docker stop postgres-llmops

# 删除容器
docker rm postgres-llmops

# 删除数据卷（谨慎！）
docker volume rm pg_data
```

## 8. 数据库迁移

项目使用 Alembic 进行数据库版本管理和迁移。

### 8.1 初始化迁移环境

首次使用时需要初始化：

```bash
flask --app app.http.app db init
```

执行后会在 `internal/migration/` 下生成迁移环境文件。

### 8.2 生成迁移脚本

修改模型后，生成迁移脚本：

```bash
# 生成迁移脚本（自动检测模型变更）
flask --app app.http.app db migrate -m "描述变更内容"
```

**示例**:
```bash
flask --app app.http.app db migrate -m "添加 app 表"
flask --app app.http.app db migrate -m "添加 status 字段"
```

生成的迁移文件位于 `internal/migration/versions/` 目录。

### 8.3 应用迁移

将迁移应用到数据库：

```bash
# 应用所有待执行的迁移
flask --app app.http.app db upgrade
```

### 8.4 回滚迁移

回滚到上一个版本：

```bash
flask --app app.http.app db downgrade
```

**警告**: 回滚操作可能导致数据丢失，请谨慎操作！

### 8.5 查看迁移历史

```bash
# 查看当前数据库版本
flask --app app.http.app db current

# 查看所有迁移历史
flask --app app.http.app db history
```

## 9. 运行命令

### 9.1 安装依赖

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 9.2 配置环境变量

创建 `.env` 文件（参考第 6 节）：

```bash
touch .env
# 编辑 .env 文件，填入实际配置
```

### 9.3 初始化数据库

首次运行需要初始化数据库：

```bash
# 初始化迁移环境（仅需执行一次）
flask --app app.http.app db init

# 生成迁移脚本
flask --app app.http.app db migrate -m "初始化数据库"

# 应用迁移
flask --app app.http.app db upgrade
```

### 9.4 启动应用

**方式一: 直接运行 Python 模块**
```bash
python -m app.http.app
```

**方式二: 使用 Flask 命令**
```bash
flask --app app.http.app run
```

**方式三: 指定端口和主机**
```bash
flask --app app.http.app run --host=0.0.0.0 --port=5000
```

**方式四: 生产环境 (使用 Gunicorn)**
```bash
# 安装 gunicorn
pip install gunicorn

# 启动服务（4 个 worker 进程）
gunicorn -w 4 -b 0.0.0.0:5000 'app.http.app:create_app()'
```

### 9.5 常用运行参数

| 参数 | 说明 |
|------|------|
| `--host 0.0.0.0` | 允许外部访问 |
| `--port 5000` | 指定端口 |
| `--debug` | 开启调试模式（自动重载） |
| `--reload` | 代码变更自动重启 |

## 10. 测试

### 3. 启动 PostgreSQL
```bash
# 使用 Docker 快速启动
docker run -d \
  --name postgres-llmops \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=123456 \
  -e POSTGRES_DB=llmops \
  -v pg_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16
```

### 4. 安装依赖
```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 5. 数据库初始化
```bash
# 初始化迁移环境
flask --app app.http.app db init

# 生成迁移脚本
flask --app app.http.app db migrate -m "初始化数据库"

# 应用迁移
flask --app app.http.app db upgrade
```

### 6. 启动应用
```bash
# 方法1: 直接运行
python -m app.http.app

# 方法2: Flask 命令
flask --app app.http.app run
```

### API 接口列表

| 接口 | 方法 | 功能描述 |
|-----|------|----------|
| `/ping` | GET | 健康检查接口 |
| `/app/completion` | POST | AI 对话补全 |
| `/app` | POST | 创建新应用 |
| `/app/<id>` | GET | 获取应用详情 |
| `/app/<id>` | POST | 更新应用信息 |
| `/app/<id>/delete` | POST | 删除应用 |

### API 详细说明

#### 5.1 健康检查
**接口**: `GET /ping`

**说明**: 测试服务是否正常运行

**响应示例**:
```json
{
  "code": "FAIL",
  "message": "数据未找到",
  "data": {}
}
```

#### 5.2 AI 对话补全
**接口**: `POST /app/completion`

**说明**: 调用 Moonshot AI API 进行对话补全

**请求参数**:
```json
{
  "query": "你好，你是谁"
}
```

**参数验证**:
- `query` (string, 必填): 用户提问，最大长度 2000 字符

**响应示例**:
```json
{
  "code": "SUCCESS",
  "message": "",
  "data": {
    "content": "我是 Kimi，由 Moonshot AI 提供的人工智能助手..."
  }
}
```

**特性**:
- 使用 kimi-k2-turbo-preview 模型
- 自动设置系统提示词
- temperature=0.6 控制生成随机性

#### 5.3 创建应用
**接口**: `POST /app`

**说明**: 创建一个新的应用记录

**请求体**: 无需参数，自动生成应用信息

**响应示例**:
```json
{
  "code": "SUCCESS",
  "message": "应用已经成功创建，id 为 123e4567-e89b-12d3-a456-426614174000",
  "data": {}
}
```

**自动生成字段**:
- `id`: UUID 格式
- `name`: 默认 "bot"
- `account_id`: 随机 UUID
- `icon`: 空字符串
- `description`: "A simple bot"
- `status`: 空字符串
- `created_at`, `update_at`: 当前时间

#### 5.4 获取应用
**接口**: `GET /app/<id>`

**说明**: 根据 UUID 获取应用详情

**路径参数**:
- `id` (UUID, 必填): 应用 ID

**响应示例**:
```json
{
  "code": "SUCCESS",
  "message": "应用已经成功获取，名字是bot",
  "data": {}
}
```

#### 5.5 更新应用
**接口**: `POST /app/<id>`

**说明**: 更新应用信息（当前版本固定修改 name 为 "bot1"）

**路径参数**:
- `id` (UUID, 必填): 应用 ID

**响应示例**:
```json
{
  "code": "SUCCESS",
  "message": "应用已经成功修改，名字是bot1",
  "data": {}
}
```

#### 5.6 删除应用
**接口**: `POST /app/<id>/delete`

**说明**: 删除指定的应用记录

**路径参数**:
- `id` (UUID, 必填): 应用 ID

**响应示例**:
```json
{
  "code": "SUCCESS",
  "message": "应用已经成功删除，id 为123e4567-e89b-12d3-a456-426614174000",
  "data": {}
}
```

### 响应状态码说明

| Code | 说明 |
|------|------|
| `SUCCESS` | 操作成功 |
| `FAIL` | 操作失败 |
| `VALIDATE_ERROR` | 请求参数验证失败 |
| `NOT_FOUND` | 资源未找到 |
| `UNAUTHORIZED` | 未授权 |
| `FORBIDDEN` | 禁止访问 |

## 6. 环境配置

### 项目目录结构

```
./
├── app/http/                 # 应用入口
│   └── app.py               # Flask 应用工厂 + Injector 配置
├── config/                   # 配置管理
│   ├── config.py            # 配置加载器（环境变量优先）
│   └── default_config.py    # 默认配置值
├── internal/                 # 核心业务逻辑（分层架构）
│   ├── router/              # 路由层
│   │   └── router.py        # Blueprint 路由注册
│   ├── handler/             # 控制器层
│   │   └── app_handler.py   # HTTP 请求处理器 + OpenAI 集成
│   ├── service/             # 业务逻辑层
│   │   └── app_service.py   # 应用 CRUD 业务逻辑
│   ├── model/               # 数据模型层
│   │   └── app.py           # App 数据表模型
│   ├── schema/              # 请求验证层
│   │   └── app_schema.py    # WTForms 验证表单
│   ├── server/              # 服务器配置
│   │   └── http.py          # Flask 应用包装器 + 异常处理
│   ├── extension/           # Flask 扩展
│   │   ├── database_extension.py  # SQLAlchemy 实例
│   │   └── migrate_extension.py   # Alembic 迁移实例
│   ├── exception/           # 异常处理
│   │   └── exception.py     # 自定义异常类
│   ├── migration/           # 数据库迁移文件
│   │   └── versions/        # Alembic 迁移脚本
│   ├── core/                # 核心模块（待实现）
│   ├── middleware/          # 中间件（待实现）
│   ├── schedule/            # 定时任务（待实现）
│   └── task/                # 异步任务（待实现）
├── pkg/                      # 共享工具包
│   ├── response/            # 响应工具
│   │   ├── response.py      # Response 数据类 + 响应辅助函数
│   │   └── http_code.py     # HTTP 状态码枚举
│   └── sqlalchemy/          # 数据库工具
│       └── sqlalchemy.py    # 自定义 SQLAlchemy 包装器（含 auto_commit）
├── test/                     # 测试文件
│   └── internal/
│       └── handler/
│           └── test_app_handler.py  # Handler 层测试
├── study/                    # LangChain 学习资料
├── Insomnia.yaml            # Insomnia API 测试集合
├── requirements.txt         # Python 依赖
└── README.md               # 项目文档
```

### 目录说明

| 目录/文件 | 说明 |
|----------|------|
| `app/http/` | 应用启动入口，配置 Flask 和 Injector |
| `config/` | 环境配置管理，支持环境变量覆盖 |
| `internal/router/` | 定义所有 API 端点，使用 Blueprint 组织 |
| `internal/handler/` | HTTP 控制器，处理请求参数、调用 Service |
| `internal/service/` | 业务逻辑层，实现 CRUD 操作 |
| `internal/model/` | SQLAlchemy ORM 模型定义 |
| `internal/schema/` | WTForms 验证表单，用于请求参数校验 |
| `pkg/response/` | 统一的 JSON 响应工具 |
| `pkg/sqlalchemy/` | 数据库工具，提供事务管理 |
| `test/` | 单元测试和集成测试 |
| `Insomnia.yaml` | API 接口测试集合，可导入 Insomnia 客户端 |

## 5. API 端点

### 10.1 使用 Insomnia 测试

项目提供了 `Insomnia.yaml` 文件，包含所有 API 接口的测试用例。

**导入步骤**:

1. 打开 Insomnia 客户端
2. 点击 "Application" → "Import/Export" → "Import Data"
3. 选择 `From File`，上传 `Insomnia.yaml`
4. 配置环境变量：
   - `BASE_URL`: `http://127.0.0.1:5000`
   - `APP_ID`: 替换为实际的应用 UUID

**测试用例列表**:

| 接口名称 | 方法 | 路径 | 说明 |
|---------|------|------|------|
| ping | GET | `/ping` | 健康检查 |
| completion | POST | `/app/completion` | AI 对话补全 |
| create_app | POST | `/app` | 创建新应用 |
| get_app | GET | `/app/{{APP_ID}}` | 获取应用详情 |
| update_app | POST | `/app/{{APP_ID}}` | 更新应用信息 |
| delete_app | POST | `/app/{{APP_ID}}/delete` | 删除应用 |

**测试示例**:

```bash
# 使用 curl 测试
curl -X GET http://127.0.0.1:5000/ping

curl -X POST http://127.0.0.1:5000/app/completion \
  -H "Content-Type: application/json" \
  -d '{"query": "你好"}'

curl -X POST http://127.0.0.1:5000/app

curl http://127.0.0.1:5000/app/<应用-ID>
```

### 10.2 单元测试

项目使用 Pytest 进行单元测试。

**运行测试**:

```bash
# 运行所有测试
pytest -v -s

# 运行特定测试文件
pytest test/internal/handler/test_app_handler.py -v -s

# 运行特定测试用例
pytest test/internal/handler/test_app_handler.py::test_ping -v -s

# 查看测试覆盖率
pytest --cov=internal --cov-report=html
```

**测试结构**:
```
test/
└── internal/
    └── handler/
        └── test_app_handler.py  # Handler 层测试
```

## 11. 开发指南

### 11.1 代码规范

**分层架构原则**:
- Router 层：只负责路由注册，不包含业务逻辑
- Handler 层：处理 HTTP 请求，调用 Service 层，返回响应
- Service 层：实现业务逻辑，数据库操作
- Model 层：定义数据模型，不包含业务逻辑

**依赖注入模式**:
```python
from injector import inject
from dataclasses import dataclass

@inject
@dataclass
class MyHandler:
    my_service: MyService  # 自动注入依赖
```

**数据库事务**:
```python
from pkg.sqlalchemy import SQLAlchemy

# 使用 auto_commit 上下文管理器
with self.db.auto_commit():
    # 数据库操作
    self.db.session.add(obj)
    self.db.session.delete(obj)
    obj.field = new_value
# 自动提交或回滚
```

**异常处理**:
```python
from internal.exception import FailException, NotFoundException

# 抛出自定义异常
raise FailException("操作失败")
raise NotFoundException("资源未找到")
```

**请求验证**:
```python
from flask import request
from internal.schema import MyForm

def my_handler():
    form = MyForm()
    if not form.validate():
        return validate_error_json(form.errors)
    # 继续处理
```

### 11.2 添加新功能流程

假设要添加一个用户管理功能：

1. **定义模型** (`internal/model/user.py`):
   ```python
   from internal.extension.database_extension import db

   class User(db.Model):
       __tablename__ = 'user'
       id = Column(UUID, primary_key=True)
       name = Column(String(255))
   ```

2. **创建验证表单** (`internal/schema/user_schema.py`):
   ```python
   class UserForm(FlaskForm):
       name = StringField('name', validators=[DataRequired()])
   ```

3. **实现业务逻辑** (`internal/service/user_service.py`):
   ```python
   @inject
   @dataclass
   class UserService:
       db: SQLAlchemy

       def create_user(self, name):
           with self.db.auto_commit():
               user = User(name=name)
               self.db.session.add(user)
           return user
   ```

4. **创建控制器** (`internal/handler/user_handler.py`):
   ```python
   @inject
   @dataclass
   class UserHandler:
       user_service: UserService

       def create_user(self):
           # 处理请求，调用 service
           pass
   ```

5. **注册路由** (`internal/router/router.py`):
   ```python
   bp.add_url_rule('/user', methods=['POST'], view_func=self.user_handler.create_user)
   ```

6. **注册依赖** (`app/http/app.py`):
   ```python
   binder.bind(UserService, UserService())
   binder.bind(UserHandler, UserHandler())
   ```

7. **生成数据库迁移**:
   ```bash
   flask --app app.http.app db migrate -m "添加 user 表"
   flask --app app.http.app db upgrade
   ```

### 11.3 数据库模型设计规范

- **主键**: 使用 UUID 类型（`Column(UUID)`）
- **时间戳**: 所有表必须包含 `created_at` 和 `updated_at`
- **默认值**: 使用 `default=` 而非 `server_default=`
- **索引**: 为常用查询字段添加索引（如 `account_id`）

**示例**:
```python
from sqlalchemy import Column, UUID, String, DateTime
import uuid
from datetime import datetime

class App(db.Model):
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID, nullable=False)
    name = Column(String(255), default="", nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
```

## 12. 常见问题

### Q1: 数据库连接失败
**症状**: `psycopg2.OperationalError`

**解决方案**:
1. 检查 PostgreSQL 是否运行: `docker ps | grep postgres-llmops`
2. 检查连接字符串是否正确: `.env` 文件中的 `SQLALCHEMY_DATABASE_URI`
3. 检查端口是否占用: `lsof -i :5432`
4. 检查用户名密码是否匹配

### Q2: API 调用失败
**症状**: AI 对话返回错误

**解决方案**:
1. 确认 `.env` 文件中 `OPEN_API_KEY` 已配置
2. 验证 API 密钥是否有效（访问 Moonshot AI 控制台）
3. 检查网络连接是否正常
4. 查看完整错误信息

### Q3: 迁移报错
**症状**: `alembic.util.exc.CommandError`

**解决方案**:
1. 确保数据库已初始化: `flask db init`
2. 检查迁移文件是否存在: `ls internal/migration/versions/`
3. 如果数据库已存在数据，可尝试清空后重新初始化
4. 检查模型定义是否正确

### Q4: 依赖注入失败
**症状**: `injector.UnsatisfiedRequirement`

**解决方案**:
1. 确保在 `app/http/app.py` 中注册了所有依赖
2. 检查依赖类的 `@inject` 和 `@dataclass` 装饰器
3. 确保依赖链完整（Handler → Service → DB）

### Q5: 端口被占用
**症状**: `Address already in use`

**解决方案**:
```bash
# 查看占用 5000 端口的进程
lsof -i :5000

# 杀死进程
kill -9 <PID>

# 或者使用其他端口
flask --app app.http.app run --port 5001
```

## 13. 项目扩展

### 计划中的功能

以下目录已预留但未实现，可在后续版本中扩展：

| 目录 | 预期功能 |
|------|----------|
| `internal/core/` | 核心业务逻辑 |
| `internal/middleware/` | 中间件（认证、日志等） |
| `internal/schedule/` | 定时任务 |
| `internal/task/` | 异步任务（Celery 等） |

### 扩展建议

1. **用户认证**: 使用 JWT 或 OAuth2
2. **日志管理**: 集成 ELK 或 Loki
3. **缓存**: 添加 Redis 缓存层
4. **消息队列**: 使用 Celery 处理异步任务
5. **API 文档**: 集成 Swagger/OpenAPI
6. **监控**: Prometheus + Grafana
7. **CI/CD**: GitHub Actions 或 GitLab CI

## 14. 相关链接

- [AGENTS.md](./AGENTS.md) - 项目详细文档
- [internal/AGENTS.md](./internal/AGENTS.md) - 核心业务逻辑文档
- [pkg/AGENTS.md](./pkg/AGENTS.md) - 共享工具文档
- [app/AGENTS.md](./app/AGENTS.md) - 应用入口文档
- [Moonshot AI 文档](https://platform.moonshot.cn/docs)
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [SQLAlchemy 文档](https://www.sqlalchemy.org/)
- [Alembic 文档](https://alembic.sqlalchemy.org/)

## 15. 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 提交规范

采用 Conventional Commits 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型 (type)**:
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构（既不是新功能也不是修复）
- `test`: 添加测试
- `chore`: 构建过程或辅助工具的变动

**示例**:
```
feat(handler): 添加用户认证接口

实现 JWT token 验证和用户登录功能

Closes #123
```

### 开发流程

1. Fork 本仓库
2. 创建功能分支: `git checkout -b feature/my-feature`
3. 提交变更: `git commit -m 'feat: add some feature'`
4. 推送到分支: `git push origin feature/my-feature`
5. 创建 Pull Request

### 代码审查要点

- ✅ 遵循分层架构
- ✅ 使用依赖注入
- ✅ 添加错误处理
- ✅ 编写测试用例
- ✅ 更新相关文档
- ✅ 代码格式规范（使用 Black/autopep8）

---

**Happy coding! 🚀**

## 🔧 开发指南

### 代码规范
- **分层架构**: 严格遵循 Router → Handler → Service → Model
- **依赖注入**: 使用 `@inject` + `@dataclass` 装饰器
- **数据库操作**: 使用 `auto_commit()` 上下文管理器
- **异常处理**: 抛出自定义异常，自动序列化为 JSON
- **请求验证**: 使用 WTForms 进行表单验证

### 添加新功能
1. **定义路由**: 在 `internal/router/router.py` 添加端点
2. **创建处理器**: 在 `internal/handler/` 添加处理器类
3. **实现业务逻辑**: 在 `internal/service/` 添加服务类
4. **定义模型**: 在 `internal/model/` 添加数据模型
5. **创建验证**: 在 `internal/schema/` 添加表单验证

### 数据库迁移
```bash
# 修改模型后生成迁移
flask --app app.http.app db migrate -m "描述变更"

# 应用迁移
flask --app app.http.app db upgrade

# 回滚迁移（谨慎使用）
flask --app app.http.app db downgrade
```

## 🤝 贡献指南

### 提交规范
- **格式**: `type: description`
- **类型**: feat(新功能), fix(修复), docs(文档), style(格式), refactor(重构), test(测试)
- **示例**: `feat: add user authentication`, `fix: resolve database connection issue`

### 开发流程
1. Fork 项目并创建功能分支
2. 编写代码并添加测试
3. 确保所有测试通过
4. 提交清晰规范的 commit
5. 创建 Pull Request

### 代码审查要点
- ✅ 遵循分层架构
- ✅ 使用依赖注入
- ✅ 添加错误处理
- ✅ 编写测试用例
- ✅ 更新文档（如需要）

## 📚 相关链接

- [AGENTS.md](./AGENTS.md) - 详细项目文档
- [内部架构文档](./internal/AGENTS.md) - 核心业务逻辑说明
- [工具文档](./pkg/AGENTS.md) - 共享工具说明
- [入口文档](./app/AGENTS.md) - 应用入口说明

## 📝 注意事项

1. **数据库**: 确保 PostgreSQL 正常运行
2. **API 密钥**: 月之暗面 API 密钥必需
3. **开发环境**: 建议启用 `FLASK_DEBUG=1` 和 `SQLALCHEMY_ECHO=True`
4. **生产环境**: 关闭调试，启用 CSRF 保护
5. **迁移**: 模型变更后务必生成和应用迁移

## 🐛 常见问题

**Q: 数据库连接失败？**
A: 检查 PostgreSQL 是否运行，用户名密码是否正确

**Q: API 调用失败？**
A: 确认 `.env` 中 `OPEN_API_KEY` 是否配置正确

**Q: 迁移报错？**
A: 确保数据库为空或迁移版本正确

---

**Happy coding! 🚀**