# Book Scents Backend

Book Scents 项目的后端服务，基于 Flask 框架开发，提供书籍管理、用户认证和评论功能的 RESTful API。

## 技术栈

- Python 3.9+
- Flask 3.0+
- MySQL 8.0
- Docker & Docker Compose
- 原生 SQL（不使用 ORM）

## 功能特性

1. **用户管理**
   - 用户注册
   - 用户登录（JWT 认证）
   - 获取用户信息

2. **书籍管理**
   - 获取书籍列表（支持分页、搜索、排序）
   - 获取书籍详情（包含评分统计）
   - 上传书籍（支持封面图片上传）
   - 记录阅读次数

3. **评论管理**
   - 获取书籍评论列表
   - 添加评论和评分

## 项目结构

```
backend/
├── .env                # 环境变量配置
├── .gitignore          # Git 忽略文件
├── Dockerfile          # Docker 构建文件
├── README.md           # 项目说明文档
├── app.py              # 主应用程序文件
├── db_init.py          # 数据库初始化脚本
├── docker-compose.yml  # Docker 容器编排配置
├── pyproject.toml      # 项目依赖配置
└── static/             # 静态文件目录
    ├── book-scents.openapi.json  # API 文档
    └── uploads/        # 上传文件存储目录
```

## 快速开始

### 使用 Docker Compose 运行

1. 确保已安装 Docker 和 Docker Compose

2. 克隆项目并进入 backend 目录

3. 运行以下命令启动服务：

   ```bash
   docker-compose up -d --build
   ```

4. 服务将在 http://localhost:5000 启动

### 本地开发

1. 确保已安装 Python 3.9+ 和 MySQL 8.0

2. 克隆项目并进入 backend 目录

3. 安装依赖：

   ```bash
   pip install poetry
   poetry install
   ```

4. 配置环境变量：
   - 复制 `.env` 文件并根据实际情况修改配置

5. 初始化数据库：

   ```bash
   python db_init.py
   ```

6. 运行开发服务器：

   ```bash
   python app.py
   ```

## API 文档

API 文档位于 `static/book-scents.openapi.json`，可使用 Swagger UI 或其他 OpenAPI 工具查看。

## 环境变量配置

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| DB_HOST | 数据库主机 | localhost |
| DB_PORT | 数据库端口 | 3306 |
| DB_USER | 数据库用户名 | root |
| DB_PASSWORD | 数据库密码 | root |
| DB_NAME | 数据库名 | book_scents |
| FLASK_APP | Flask 应用入口 | app.py |
| FLASK_ENV | Flask 运行环境 | development |
| SECRET_KEY | Flask 密钥 | your-secret-key-here |
| JWT_SECRET_KEY | JWT 密钥 | your-jwt-secret-key-here |
| UPLOAD_FOLDER | 上传文件目录 | ./static/uploads |
| MAX_CONTENT_LENGTH | 最大上传文件大小 | 16*1024*1024 (16MB) |

## 注意事项

1. 文件上传功能使用本地存储，上传的文件保存在 `static/uploads` 目录下

2. 开发环境下，Flask 会以调试模式运行

3. 生产环境中，建议使用 Gunicorn 等 WSGI 服务器部署

4. 生产环境中，请确保修改 `.env` 文件中的密钥和密码为安全的值

## 数据库表结构

1. **users** - 用户表
2. **books** - 书籍表
3. **comments** - 评论表

数据库初始化脚本会自动创建这些表。