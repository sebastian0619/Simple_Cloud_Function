# 使用官方 Python 镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到容器内
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 从环境变量中读取额外依赖并安装
ARG EXTRA_REQUIREMENTS
RUN if [ -n "$EXTRA_REQUIREMENTS" ]; then \
        pip install --no-cache-dir $EXTRA_REQUIREMENTS; \
    fi

# 暴露端口
EXPOSE 8888

# 启动应用
CMD ["python", "app.py"]