# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Poetry
RUN pip install --no-cache-dir poetry==1.6.1

# 复制 pyproject.toml 和 poetry.lock（如果有）
COPY pyproject.toml* poetry.lock* ./

# 配置 Poetry 不创建虚拟环境
RUN poetry config virtualenvs.create false

# 安装项目依赖
RUN poetry install --no-dev --no-interaction --no-ansi

# 复制项目文件
COPY . .

# 创建静态文件目录和上传目录
RUN mkdir -p ./static/uploads

# 暴露端口
EXPOSE 5000

# 启动应用程序
CMD ["python", "app.py"]