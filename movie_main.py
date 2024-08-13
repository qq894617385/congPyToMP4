from congMovice.sound import make_sound
from congMovice.captions import create_video_from_json, merge_video_by_projectName


def main_create(projectName, socketio, allCreate=True):
    try:

        print('开始生成音频')
        workSpacePath = projectName
        socketio.emit('update', {'data': f'开始制作 {projectName}'})

        print('开始生成视频')
        make_sound(workSpacePath)
        socketio.emit('update', {'data': f'生成音频{projectName}成功.'})

        print('开始完成')
        create_video_from_json(workSpacePath, allCreate)
        socketio.emit('update', {'data': f'项目{projectName}合成完成.'})

    except Exception as e:
        print(f'An error occurred: {e}')
        # 发送错误信息到前端
        socketio.emit('error', {'error': str(e)})
        # 可以考虑将错误记录到日志文件，便于后续分析和问题排查


def merge_video(projectName, socketio):
    print('开始合成视频')
    workSpacePath = projectName
    socketio.emit('update', {'data': f'开始合成--{projectName}'})
    merge_video_by_projectName(workSpacePath)
    socketio.emit('update', {'data': f'合成成功--{projectName}'})
