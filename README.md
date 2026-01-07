# llmops

`.env`
```dotenv
OPEN_API_KEY=sk-xxx
OPEN_API_BASE=https://api.moonshot.cn/v1

FLASK_DEBUG=1
FLASK_ENV=development

WTF_CSRF_ENABLED=False

SQLALCHEMY_DATABASE_URI=postgresql://root:123456@localhost:5432/llmops
SQLALCHEMY_POOL_SIZE=30
SQLALCHEMY_POOL_RECYCLE=3600
SQLALCHEMY_ECHO=True
```

```shell
docker run -d \
  --name postgres-llmops \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=123456 \
  -e POSTGRES_DB=llmops \
  -v pg_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16
```

```shell
# 初始化迁移环境
flask --app app.http.app db init

# 生成迁移脚本
flask --app app.http.app db migrate

# 更新数据库
flask --app app.http.app db upgrade

# 回滚数据库
flask --app app.http.app db downgrade
flask --app app.http.app db downgrade base
flask --app app.http.app db downgrade <version>
```