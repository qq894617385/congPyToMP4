import os
import cv2
import math
import numpy as np


def make_background_video(total_time, workSpacePath):
    current_directory = os.path.join(os.getcwd(), 'dataSpace', workSpacePath)
    # 获取存放图片的文件夹路径
    imagePath = os.path.join(current_directory, 'images')

    # 设置视频输出文件夹路径
    output_directory = os.path.join(current_directory, 'video')
    os.makedirs(output_directory, exist_ok=True)
    video_name = 'output.mp4'

    # 获取图片列表，仅包括图片文件
    image_files = [f for f in os.listdir(imagePath) if f.endswith((".jpg", ".jpeg", ".png"))]

    print(image_files)

    num_of_images = len(image_files)

    # 计算每张图片停留时间
    video_secs = math.ceil(total_time / num_of_images) * 24

    # 设置视频编码器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # 设置目标视频尺寸
    target_width, target_height = 640, 640

    # 创建视频写入对象
    output_path = os.path.join(output_directory, video_name)
    video = cv2.VideoWriter(output_path, fourcc, 24, (target_width, target_height))  # 帧率设置为24

    black_image = np.zeros((640, 640, 3), dtype=np.uint8)

    # 遍历图片列表，生成视频
    for image_name in image_files:
        image_path = os.path.join(imagePath, image_name)
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法读取图片：{image_path}")
            continue
        height, width, _ = image.shape

        # 计算调整后的图像尺寸
        if height < width:
            scaled_image = cv2.resize(image, (target_width, int(height * (target_width / width))))
            top_pad = max((target_height - scaled_image.shape[0]) // 2, 0)
            bottom_pad = max(target_height - scaled_image.shape[0] - top_pad, 0)
            left_pad, right_pad = 0, 0
        else:
            scaled_image = cv2.resize(image, (int(width * (target_height / height)), target_height))
            left_pad = max((target_width - scaled_image.shape[1]) // 2, 0)
            right_pad = max(target_width - scaled_image.shape[1] - left_pad, 0)
            top_pad, bottom_pad = 0, 0

        # 图像填充
        padded_image = cv2.copyMakeBorder(scaled_image, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT,
                                          value=(0, 0, 0))
        scale_factor = 1
        # 将调整后的图像写入视频
        for a in range(video_secs):
            if a <= 20:  # 前10帧为淡入效果
                alpha = a * 0.05
                alpha_image = cv2.addWeighted(black_image, 1 - alpha, padded_image, alpha, 0)
            elif a >= video_secs - 20:  # 后10帧为淡出效果
                # 保持未放大完的效果
                resized_image = cv2.resize(padded_image, None, fx=scale_factor, fy=scale_factor,
                                           interpolation=cv2.INTER_LINEAR)
                x_offset = max((resized_image.shape[1] - target_width) // 2, 0)
                y_offset = max((resized_image.shape[0] - target_height) // 2, 0)
                padded_image = resized_image[y_offset:y_offset + target_height, x_offset:x_offset + target_width]

                alpha = (video_secs - a) * 0.05
                alpha_image = cv2.addWeighted(padded_image, alpha, black_image, 1 - alpha, 0)
            else:  # 中间帧保持不变
                scale_factor = min(1.3, 1 + (a - 20) * 0.02)  # 限制放大倍数不超过1.6
                resized_image = cv2.resize(padded_image, None, fx=scale_factor, fy=scale_factor,
                                           interpolation=cv2.INTER_LINEAR)
                x_offset = max((resized_image.shape[1] - target_width) // 2, 0)
                y_offset = max((resized_image.shape[0] - target_height) // 2, 0)
                alpha_image = resized_image[y_offset:y_offset + target_height, x_offset:x_offset + target_width]

            video.write(alpha_image)

    # 释放资源
    video.release()
    cv2.destroyAllWindows()

    print('输出完成')

# make_background_video(252, 'raw')
