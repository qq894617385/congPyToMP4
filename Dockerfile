# 使用官方 Python 3.11-slim 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive

# 更新包管理器并安装系统依赖项
RUN apt-get update && apt-get install -y \
    libmediainfo0v5 \
    imagemagick \
    libgl1 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 安装 Python 包
RUN pip install --no-cache-dir Flask TTS flask_cors pymediainfo opencv-python moviepy numpy flask-socketio diffusers transformers sentencepiece accelerate

# 修改 ImageMagick 的 policy.xml 文件中的限制
RUN sed -i 's/<policy domain="path" rights="none" pattern="@\*"/<policy domain="path" rights="read|write" pattern=""/g' /etc/ImageMagick-6/policy.xml

# 设置工作目录并复制应用程序文件
COPY . .

# 运行 Flask 应用
CMD ["python", "app.py"]
