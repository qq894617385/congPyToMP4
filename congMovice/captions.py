from moviepy.editor import *
from congMovice.utils import wrap_text
import os
import json


def create_video_from_json(workSpacePath, allCreate=True):
    root_path = os.environ['root']
    current_directory = os.path.join(root_path, 'dataSpace', workSpacePath)
    jsonPath = os.path.join(current_directory, 'index.json')

    # 加载 JSON 文件
    with open(jsonPath, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    output_directory = os.path.join(current_directory, "output")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    video_directory = os.path.join(current_directory, "video")
    if not os.path.exists(video_directory):
        os.makedirs(video_directory)

    # 清除video_directory下面的所有文件
    for file in os.listdir(video_directory):
        os.remove(os.path.join(video_directory, file))

    temp_files = []
    width = json_data['project']['width'] or 640
    height = json_data['project']['height'] or 640

    # 背景音乐和图片目录
    mp3_directory = os.path.join(current_directory, "sounds")

    for idx, item in enumerate(json_data['textArr']):
        text = item['text']
        bg_image_path = os.path.join(current_directory, "images", item['bgi'])

        # 读取配音文件
        mp3_path = os.path.join(mp3_directory, f"{idx}.mp3")
        audio_clip = AudioFileClip(mp3_path)
        audio_duration = audio_clip.duration  # 获取音频持续时间
        print(f"{audio_duration} 多少秒")

        # 加载背景图片并设置持续时间为音频持续时间
        bg_image_clip = ImageClip(bg_image_path).set_duration(audio_duration)

        # 获取图像尺寸并根据宽高比调整大小
        img_width, img_height = bg_image_clip.size
        if img_width > img_height:
            scale_factor = width / float(img_width)
        else:
            scale_factor = height / float(img_height)
        new_size = (int(img_width * scale_factor), int(img_height * scale_factor))

        # 调整图片大小并保持比例
        bg_image_clip = bg_image_clip.resize(new_size)

        # 创建一个 640x640 的黑色背景
        bg_color_clip = ColorClip(size=(width, height), color=(0, 0, 0), duration=audio_duration)

        # 将调整后的图片居中放置在黑色背景上
        combined_clip = CompositeVideoClip([bg_color_clip, bg_image_clip.set_position("center")], size=(width, height))

        bgc = item['bgc'] or 'black'
        fontSize = item['fontSize'] or 24
        color = item['color'] or 'white'

        # 创建文字剪辑，并设置持续时间为音频持续时间
        txt_clip = TextClip(text, fontsize=fontSize, color=color, bg_color=bgc, font='SimHei').set_position(
            'center').set_duration(audio_duration)

        # 文字剪辑的位置，距离底部 text_bottom_margin 像素
        text_bottom_margin = item['marginBottom'] or 60  # 可以根据需要调整这个值
        text_position = ('center', height - text_bottom_margin)

        # 将文字剪辑合成到背景图片上
        combined_clip = CompositeVideoClip([combined_clip, txt_clip.set_position(text_position)])
        combined_clip = combined_clip.set_audio(audio_clip)  # 设置音频

        # 输出每个视频剪辑到临时文件
        temp_file = os.path.join(video_directory, f"{idx}.mp4")
        combined_clip.write_videofile(temp_file, codec='libx264', fps=24)
        temp_files.append(temp_file)

        # 关闭剪辑以释放资源
        combined_clip.close()
        audio_clip.close()
    # 全部生成
    if allCreate:
        # 读取所有临时文件并合成最终视频
        clips = [VideoFileClip(temp_file) for temp_file in temp_files]
        final_clip = concatenate_videoclips(clips, method="compose")

        # 输出最终视频
        final_output = os.path.join(output_directory, "final_output.mp4")
        final_clip.write_videofile(final_output, codec='libx264', fps=24)

        # 关闭所有剪辑并删除临时文件
        final_clip.close()
        for clip in clips:
            clip.close()

        print("视频已成功生成：", final_output)


def merge_video_by_projectName(workSpacePath):
    root_path = os.environ['root']
    current_directory = os.path.join(root_path, 'dataSpace', workSpacePath)
    video_directory = os.path.join(current_directory, "video")
    output_directory = os.path.join(current_directory, "output")

    # 读取所有临时文件并合成最终视频
    temp_files = [os.path.join(video_directory, file) for file in os.listdir(video_directory) if file.endswith('.mp4')]
    clips = [VideoFileClip(temp_file) for temp_file in temp_files]
    final_clip = concatenate_videoclips(clips, method="compose")

    # 输出最终视频
    final_output = os.path.join(output_directory, "final_output.mp4")
    final_clip.write_videofile(final_output, codec='libx264', fps=24)

    # 关闭所有剪辑并删除临时文件
    final_clip.close()
    for clip in clips:
        clip.close()

    print("视频已成功生成：", final_output)
