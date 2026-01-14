# LLM 运维平台

基于 Flask 的 LLM（大语言模型）运维管理平台，支持应用管理、AI 对话等功能。

## 🚀 项目简介

这是一个企业级的 LLM 运维平台，采用分层架构设计：
- **后端框架**: Flask + SQLAlchemy + PostgreSQL
- **架构模式**: 依赖注入 + 分层架构 (Router → Handler → Service → Model)
- **AI 集成**: 月之暗面 (Moonshot AI) API 集成
- **API 设计**: RESTful 接口，标准化响应格式

## 📋 功能特性

- ✅ 应用管理 (创建、查询、更新、删除)
- ✅ AI 对话补全功能
- ✅ 数据库迁移支持
- ✅ 统一异常处理
- ✅ 标准化 API 响应
- ✅ 依赖注入架构

## 🛠️ 快速开始

### 环境要求
- Python 3.12+
- PostgreSQL 16+
- 月之暗面 API 密钥

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd llmops
```

### 2. 配置环境变量
创建 `.env` 文件并配置：
```dotenv
# AI 服务配置
OPEN_API_KEY=sk-xxx                    # 月之暗面 API 密钥
OPEN_API_BASE=https://api.moonshot.cn/v1

# Flask 配置
FLASK_DEBUG=1                           # 开发模式
FLASK_ENV=development
WTF_CSRF_ENABLED=False                  # 开发环境关闭 CSRF

# 数据库配置
SQLALCHEMY_DATABASE_URI=postgresql://root:123456@localhost:5432/llmops
SQLALCHEMY_POOL_SIZE=30                 # 连接池大小
SQLALCHEMY_POOL_RECYCLE=3600            # 连接回收时间
SQLALCHEMY_ECHO=True                    # 打印 SQL 语句（开发用）
```

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

## 📡 API 接口

| 接口 | 方法 | 说明 |
|-----|------|------|
| `/ping` | GET | 健康检查 |
| `/app/completion` | POST | AI 对话补全 |
| `/app` | POST | 创建应用 |
| `/app/<id>` | GET | 获取应用 |
| `/app/<id>` | POST | 更新应用 |
| `/app/<id>/delete` | POST | 删除应用 |

## 🏗️ 项目结构

```
./
├── app/http/           # 应用入口（Flask 工厂模式）
├── config/             # 配置管理
├── internal/           # 核心业务逻辑
│   ├── handler/        # HTTP 请求处理器
│   ├── service/        # 业务逻辑层
│   ├── model/          # 数据模型
│   ├── router/         # 路由定义
│   └── ...
├── pkg/                # 共享工具
│   ├── response/       # 响应工具
│   └── sqlalchemy/     # 数据库工具
├── test/               # 测试文件
└── study/              # LangChain 学习资料
```

## 🧪 运行测试

```bash
# 运行所有测试
pytest -v -s

# 运行特定测试
pytest test/internal/handler/test_app_handler.py -v -s
```

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