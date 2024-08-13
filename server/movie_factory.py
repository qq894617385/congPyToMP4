from flask import request, Response, send_from_directory, abort, jsonify
from werkzeug.utils import secure_filename
from movie_main import main_create, merge_video
from concurrent.futures import ThreadPoolExecutor
from congMovice.utils import *
import os
import json
import shutil
# 引入socket
from server.mysocket import get_socketio

executor = ThreadPoolExecutor(max_workers=5)


def init_movie_factory(app):
    @app.route('/makeMovie', methods=['POST', 'GET'])
    def txt2Video():
        request_json = request.json
        if 'projectName' in request_json:
            # 将main_create函数放入线程池异步执行
            socketio = get_socketio()
            print("socketio instance:", socketio)

            executor.submit(main_create, request_json['projectName'], socketio, True)
            # 等待异步处理完成
            return jsonify({}), 200
        else:
            raise KeyError("The 'projectName' parameter is required but was not provided.")

    @app.route('/makeEveryVideo', methods=['POST', 'GET'])
    def makeEveryVideo():
        request_json = request.json
        if 'projectName' in request_json:
            # 将main_create函数放入线程池异步执行
            socketio = get_socketio()
            print("socketio instance:", socketio)

            executor.submit(main_create, request_json['projectName'], socketio, False)
            # 等待异步处理完成
            return jsonify({}), 200
        else:
            raise KeyError("The 'projectName' parameter is required but was not provided.")
    # 合并视频
    @app.route('/mergeVideo', methods=['POST', 'GET'])
    def mergeVideo():
        request_json = request.json
        if 'projectName' in request_json:
            # 将main_create函数放入线程池异步执行
            socketio = get_socketio()
            print("socketio instance:", socketio)

            executor.submit(merge_video, request_json['projectName'], socketio)
            # 等待异步处理完成
            return jsonify({}), 200
        else:
            raise KeyError("The 'projectName' parameter is required but was not provided.")

    # 获取所有项目名
    @app.route('/getProjectNameList', methods=['POST', 'GET'])
    def getProjectName():
        # 获取static目录下dataSpace文件夹下的所有文件夹
        root_path = os.environ['root']
        folders = list_subdirectories(os.path.join(root_path, 'dataSpace'))
        return folders

    # 根据项目所在的地址获取相关图片信息
    @app.route('/getProjectDetail', methods=['POST'])
    def getDetailByName():
        request_json = request.json
        root_path = os.environ['root']
        if 'projectName' in request_json:
            project_name = request_json['projectName']

            if os.path.exists(f"{root_path}/dataSpace/{project_name}"):
                file_path = f"{root_path}/dataSpace/{project_name}/index.json"
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        return data
                except FileNotFoundError:
                    print(f"Error: The file '{file_path}' does not exist.")
                    return None
                except json.JSONDecodeError:
                    print(f"Error: The file '{file_path}' is not a valid JSON.")
                    return None
            else:
                raise KeyError("不存在该项目")
        else:
            raise KeyError("丢失项目名称")

    # 读取图片
    @app.route('/images/<path:filename>')
    def get_image(filename):
        root_path = os.environ['root']
        # 指定你的图片存放路径
        image_directory = os.path.join(root_path, 'dataSpace')
        # 确保文件名安全，防止路径遍历攻击
        if not os.path.isfile(os.path.join(image_directory, filename)):
            abort(404)  # 如果文件不存在，返回 404 错误
        return send_from_directory(image_directory, filename)

    # 读取视频
    @app.route('/video/<path:projectName>')
    def get_video(projectName):
        root_path = os.environ['root']

        project_path = os.path.join(root_path, 'dataSpace', projectName)
        if os.path.exists(project_path):
            # 指定你的图片存放路径
            video_directory = os.path.join(project_path, 'output', 'final_output.mp4')
            return Response(get_video_stream(video_directory), mimetype='video/mp4')
        else:
            return jsonify({'error': '视频丢失'}), 500

    @app.route('/videoSpan/<path:projectName>/<videoName>', methods=['GET'])
    def get_video_span(projectName, videoName):
        root_path = os.environ['root']
        project_path = os.path.join(root_path, 'dataSpace', projectName)
        video_path = os.path.join(project_path, 'video', videoName + '.mp4')

        if os.path.exists(video_path):
            return Response(get_video_stream(video_path), mimetype='video/mp4')
        else:
            return jsonify({'error': '视频丢失'}), 500

    # 新建项目
    @app.route('/create_project', methods=['POST'])
    def create_project():
        project_name = request.json.get('project_name')
        if not project_name:
            return jsonify({'error': 'Project name is required'}), 400
        root_path = os.environ['root']
        project_path = os.path.join(root_path, 'dataSpace', project_name)
        # 检查项目目录是否已存在
        if os.path.exists(project_path):
            return jsonify({'code': -1, 'error': 'Project already exists'}), 409  # 409 Conflict
        try:
            # 创建项目目录
            os.makedirs(project_path, exist_ok=True)

            # 创建子目录
            subfolders = ['images', 'output', 'sounds', 'video']
            for folder in subfolders:
                os.makedirs(os.path.join(project_path, folder), exist_ok=True)

            # 读取模板json文件
            baseProjectPath = os.path.join(root_path, 'baseProject.json')
            # 获取内容
            with open(baseProjectPath, 'r', encoding='utf-8') as file:
                baseJsonData = json.load(file)

            # 创建一个 index.json 文件
            json_file_path = os.path.join(project_path, 'index.json')
            with open(json_file_path, 'w', encoding='utf-8') as file:
                baseJsonData['title'] = project_name
                baseJsonData['dict'] = project_name
                json.dump(baseJsonData, file, indent=4, ensure_ascii=False)

            return jsonify({'message': f'Project {project_name} created successfully'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # 删除项目
    @app.route('/delete_project', methods=['POST'])
    def del_project():
        project_name = request.json.get('project_name')
        if project_name:
            root_path = os.environ['root']
            project_path = os.path.join(root_path, 'dataSpace', project_name)

            # 检查路径是否存在
            if os.path.exists(project_path):
                # 尝试删除目录
                try:
                    shutil.rmtree(project_path)
                    return jsonify({'status': 'success', 'message': 'Project deleted successfully'}), 200
                except Exception as e:
                    return jsonify({'status': 'error', 'message': str(e)}), 500
            else:
                return jsonify({'status': 'error', 'message': 'Project not found'}), 404
        else:
            return jsonify({'status': 'error', 'message': 'No project name provided'}), 400

    # 上传图片
    @app.route('/upload_image/<project_name>', methods=['POST'])
    def upload_image(project_name):
        image_directory = os.path.join('dataSpace', project_name, 'images')
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(image_directory, filename))

            return jsonify({'message': 'File uploaded successfully'}), 200
        return jsonify({'error': 'Invalid file type'}), 400

    @app.route('/delete_image/<project_name>/<filename>', methods=['DELETE'])
    def delete_image(project_name, filename):
        image_path = os.path.join('dataSpace', project_name, 'images', secure_filename(filename))
        if os.path.exists(image_path):
            os.remove(image_path)
            return jsonify({'message': 'Image deleted successfully'}), 200
        return jsonify({'error': 'Image not found'}), 404

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

    @app.route('/get_project_images/<project_name>', methods=['get', 'post'])
    def get_project_images(project_name):
        root_path = os.environ['root']
        image_directory = os.path.join(root_path, 'dataSpace', project_name, 'images')
        image_files = [f for f in os.listdir(image_directory) if f.endswith((".jpg", ".jpeg", ".png"))]
        return jsonify({'images': image_files}), 200

    # 保存项目
    @app.route('/save_project/<project_name>', methods=['get', 'post'])
    def save_project(project_name):
        request_json = request.json
        root_path = os.environ['root']
        if project_name:
            project_path = os.path.join(root_path, 'dataSpace', project_name)

            baseJsonData = {}
            json_file_path = os.path.join(project_path, 'index.json')
            if os.path.exists(json_file_path):
                try:
                    with open(json_file_path, 'r', encoding='utf-8') as file:
                        baseJsonData = json.load(file)
                except FileNotFoundError:
                    print(f"Error: The file '{json_file_path}' does not exist.")
                    return None
                except json.JSONDecodeError:
                    print(f"Error: The file '{json_file_path}' is not a valid JSON.")
                    return None
            else:
                baseJsonData = {}

            # 获取传上来的数据
            if request_json['detail']:
                baseJsonData.update(request_json['detail'])
                with open(json_file_path, 'w', encoding='utf-8') as file:
                    json.dump(baseJsonData, file, indent=4, ensure_ascii=False)

        return jsonify({'msg': '保存成功'}), 200
