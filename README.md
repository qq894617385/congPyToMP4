# 项目介绍  
**Project Introduction**  
Python 项目，用于根据文本快速生成图片，并加上 Ai 配音，并可以配上背景图转换生成视频。  
*Python project for quickly generating images based on text, adding AI dubbing, and converting them into videos with background images.*

基于 Python 3.11+ 版本。  
*Based on Python 3.11+ version.*

音频模型基于 TTS。  
*Audio model based on TTS.*

图片生成模型基于 Stable Diffusion。  
*Image generation model based on Stable Diffusion.*

翻译模型基于 Transformers。  
*Translation model based on Transformers.*

## 项目运行部署  
**Project Deployment**

请自行先安装好 Python 3.11 必须要的环境，并克隆本项目。  
*Please install the required Python 3.11 environment and clone this project.*

请自行下载 models 模型（约 8G），并解压到根目录下。  
*Please download the models (about 8G) and extract them to the root directory.*

|- pythonProject  
|--- ***  
|--- congMovice  
|--- **models**  
|--- server  
|--- ***

**模型链接（百度网盘）**  
*Model Link (Baidu Cloud)*

>  *Link: https://pan.baidu.com/s/14u6CoGWTQG_vmL1gKCmLDg?pwd=pb4t  
Password: pb4t*

### 安装依赖  
**Install Dependencies**

```cmd  
pip install -r requirements.txt  
```

### 或者  
**Or**

```cmd  
pip install Flask TTS flask_cors pymediainfo opencv-python moviepy numpy flask-socketio diffusers transformers sentencepiece accelerate  
```

### 运行（本地开发环境）  
**Run (Local Development Environment)**

```cmd  
.\venv\Scripts\activate  
```

#### 进入虚拟环境  
**Enter Virtual Environment**

```cmd  
python app.py  
```

### Flask 服务  
**Flask Service**

默认 host 0.0.0.0 即本机 127.0.0.1 默认端口 5000。  
*Default host is 0.0.0.0, which means localhost 127.0.0.1, with a default port of 5000.*

**app.py**

```python  
app.run(host='0.0.0.0', port=5000, threaded=True)  
```

**static/voicelist**  
存放的刻录配音文件，也可以自己刻录自己的声音（目前前端暂无选中声音音频的功能）。  
*Stores dubbed audio files. You can also record your own voice (currently, the frontend does not have the feature to select audio files).*

如果有需要修改，请自行到 congMovice 包下面更改。  
*If you need to modify it, please change it under the congMovice package.*

```python  
outputName = os.path.join(outputPath, span_name)  
  
wav_path = os.path.join(root_path, 'voicelist/cn-sx.wav')  # 此处请可以替换 cn-sx.wav 为自己的声音  
# You can replace cn-sx.wav with your own voice here
  
last_file = tts.tts_to_file(text=text, speaker_wav=wav_path, speed=0.9, language="zh-cn",  
                            file_path=outputName)  
```

### Web 服务  
**Web Service**

默认 127.0.0.1:5000 直接访问到前端界面。  
*Default access to the frontend interface at 127.0.0.1:5000.*

```tree  
web  
 ┣ 📂css  
 ┃ ┣ 📜app.803ed75d.css  
 ┃ ┣ 📜app.a229f925.css  
 ┃ ┗ 📜chunk-vendors.b69c2035.css  
 ┣ 📂js  
 ┃ ┣ 📜about.0e8aa43d.js  
 ┃ ┣ 📜about.0e8aa43d.js.map  
 ┃ ┣ 📜app.4b0ee990.js  
 ┃ ┣ 📜app.4b0ee990.js.map  
 ┃ ┣ 📜app.b031b391.js  
 ┃ ┣ 📜app.b031b391.js.map  
 ┃ ┣ 📜app.c6ab89a5.js  
 ┃ ┣ 📜app.c6ab89a5.js.map  
 ┃ ┣ 📜chunk-vendors.28133fbc.js  
 ┃ ┣ 📜chunk-vendors.28133fbc.js.map  
 ┃ ┣ 📜chunk-vendors.ad037dda.js  
 ┃ ┗ 📜chunk-vendors.ad037dda.js.map  
 ┣ 📜favicon.ico  
 ┗ 📜index.html  
```

源码放在另一个项目。  
*The source code is in another project.*

## Docker 打包管理  
**Docker Packaging Management**

```dockerfile  
# 使用官方 Python 镜像  
# Use official Python image  
FROM python:3.11-slim  
  
# 设置工作目录  
# Set the working directory  
WORKDIR /app  
  
# 复制当前目录的内容到工作目录  
# Copy the current directory contents into the working directory  
COPY . .  
  
# 安装 Flask  
# Install Flask  
RUN pip install Flask TTS flask_cors pymediainfo opencv-python moviepy numpy flask-socketio diffusers transformers sentencepiece accelerate  
  
# 运行 Flask 应用  
# Run Flask application  
CMD ["python", "app.py"]  
```

Docker 版本 27.0.1 已经测试完成。  
*Docker version 27.0.1 has been tested successfully.*

已经复刻镜像 (20G)，开箱即用。  
*The image (20G) has been replicated and is ready to use.*

> 
*Baidu Cloud Link: https://pan.baidu.com/s/1Vkxkd7ClruBtkaIw-fWpEg?pwd=zj2l  
Password: zj2l*  

```

