import os
from datetime import datetime
import torch
from TTS.api import TTS
from pymediainfo import MediaInfo
import json
from congMovice.utils import clear_folder

device = "cpu"
tts = None


# 初始化
def sound_factory_init():
    print('正在初始化数据.....加载数据模型中')
    global device, tts

    # 获取当前目录下的static的tts文件夹
    tts_path = os.path.join(os.environ['models'])

    # Set up TTS environment
    os.environ.setdefault('TTS_HOME', tts_path)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    print(f'加载完成....{device}')


def get_media_duration(file_path):
    media_info = MediaInfo.parse(file_path)
    for track in media_info.tracks:
        if track.track_type == 'Audio':
            return track.duration


def make_sound(workSpacePath):
    print('开始生成Ai语音')
    root_path = os.environ['root']
    current_directory = os.path.join(root_path, 'dataSpace', workSpacePath)
    outputPath = os.path.join(current_directory, 'sounds')
    jsonPath = os.path.join(current_directory, 'index.json')
    mp3List = []
    start = 0

    with open(jsonPath, 'r', encoding='utf-8') as file:
        jsonData = json.load(file)
        text_arr = jsonData["textArr"]

        # 使用列表推导提取 text 字段
        textArr = [item["text"] for item in text_arr]


        print('先清空文件')
        clear_folder(outputPath)

        for index, text in enumerate(textArr):
            span_name = str(index) + '.mp3'
            current_time = datetime.now()
            outputName = os.path.join(outputPath, span_name)

            wav_path = os.path.join(root_path, 'voicelist/cn-sx.wav')

            last_file = tts.tts_to_file(text=text, speaker_wav=wav_path, speed=0.9, language="zh-cn",
                                        file_path=outputName)

            duration = get_media_duration(last_file)
            current_time1 = datetime.now()
            delta = current_time1 - current_time
            print(f"生成时间: {delta}, 文件名: {outputName}, 长度：{duration}")
            mp3List.append({
                "start": start,
                "sound": span_name,
                "duration": duration,
                "text": text
            })
            start += duration

    print('AI 语音完成')
    return mp3List
