# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到工作目录
COPY . .

# 安装 Flask
RUN pip install Flask TTS flask_cors pymediainfo opencv-python moviepy numpy flask-socketio diffusers transformers sentencepiece accelerate

# 运行 Flask 应用
CMD ["python", "app.py"]
