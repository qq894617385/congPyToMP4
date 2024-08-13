# 项目介绍
python项目，用于根据文本快速生成图片，并加上Ai配音，并可以可以配上背景图转换生成视频

基于 python 3.11+ 版本

音频模型基于tts

图片生成模型基于 stableDiffusion

翻译模型基于 transformers


## 项目运行部署

请自行先安装好python3.11 必须要的环境，并克隆本项目

请自行下载models 模型（约8G），并解压到根目录下

|- pythonProject
|--- ***
|--- congMovice
|--- **models**
|--- server
|--- ***

**模型链接（百度网盘）**

> 链接：https://pan.baidu.com/s/14u6CoGWTQG_vmL1gKCmLDg?pwd=pb4t 
提取码：pb4t


### 安装依赖

```cmd
pip install -r requirements.txt
```

### 或者
```cmd
pip install Flask TTS flask_cors pymediainfo opencv-python moviepy numpy flask-socketio diffusers transformers sentencepiece accelerate
```

### 运行（本地开发环境）
```cmd
.\venv\Scripts\activate
```
#### 进入虚拟环境
 ```cmd
 python app.py
```


### flask 服务

默认host 0.0.0.0 即本机127.0.0.1 默认端口 5000

**app.py**

```python
 app.run(host='0.0.0.0', port=5000, threaded=True)
```

**static/voicelist**
存放的刻录配音文件，也可以自己刻录自己的声音（目前前端暂无选中声音音频的功能）
如果有需要修改，请自行到 congMovice包下面更改

```python
            outputName = os.path.join(outputPath, span_name)

            wav_path = os.path.join(root_path, 'voicelist/cn-sx.wav') # 此处请可以替换cn-sx.wav为自己的声音

            last_file = tts.tts_to_file(text=text, speaker_wav=wav_path, speed=0.9, language="zh-cn",
                                        file_path=outputName)
```

### web服务
默认127.0.0.1:5000 直接访问到前端界面

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

````


 源码放在另一个项目


 ## Docker打包管理

 ```dockerfile
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

 ```

docker 版本 27.0.1 经已测试完成

已经复刻镜像(20G),开箱即用

> 百度网盘
