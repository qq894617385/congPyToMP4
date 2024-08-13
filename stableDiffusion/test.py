from flask import Flask, request, jsonify, send_file
from diffusers import StableDiffusionPipeline
import torch
import os

app = Flask(__name__)
pipeline = None


def init_model():
    global pipeline
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_cache_dir = "image_model"

    pipeline = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        cache_dir=model_cache_dir
    )
    pipeline = pipeline.to(device)


@app.route('/generate-image', methods=['POST'])
def generate_image():
    global pipeline
    content = request.json
    prompt = content.get('prompt')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    image = pipeline(prompt).images[0]

    # 保存图像到临时文件
    filename = 'generated_image.png'
    image.save(filename)

    # 可选：返回图像文件的路径或直接作为响应返回图像文件
    # return send_file(filename, mimetype='image/png')
    return jsonify({'message': 'Image generated successfully', 'filename': filename})


if __name__ == '__main__':
    init_model()  # 在服务器启动时初始化模型
    app.run(port=5001, debug=True)  # 启动 Flask 应用
