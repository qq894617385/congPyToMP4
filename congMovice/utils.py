import os
import shutil

def list_subdirectories(directory):
    """
    列出指定目录下的所有子目录名称。

    :param directory: 要遍历的目录的路径。
    :return: 包含所有子目录名称的列表。
    """
    # 确保目录是存在的
    if not os.path.exists(directory):
        print(f"指定的目录不存在: {directory}")
        return []

    # os.listdir(directory) 返回指定路径下的文件和目录列表
    # os.path.isdir(os.path.join(directory, name)) 检查指定路径是否为目录
    subdirectories = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    return subdirectories


def clear_folder(folder_path):
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # 遍历文件夹中的每个文件和子文件夹
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            # 如果是文件或链接，则删除
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"Deleted file: {file_path}")
            # 如果是文件夹，则删除整个文件夹
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Deleted folder: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def get_video_stream(path):
    """这里应该是获取视频流的逻辑，以下代码假设你有一个视频文件路径。"""
    with open(path, 'rb') as video:
        while True:
            data = video.read(1024 * 1024)  # 读取1MB大小的数据块
            if not data:
                break
            yield data


# 设置文本自动换行
def wrap_text(text):
    # 用逗号和句号分隔，并在每个分隔符后插入换行符
    wrapped_text = text.replace('，', '，\n').replace('。', '。\n')
    return wrapped_text
