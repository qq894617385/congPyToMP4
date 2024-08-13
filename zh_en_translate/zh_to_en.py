from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

tokenizer = None
model = None


def init_translate_zh_to_en():
    global tokenizer
    global model
    root_path = os.environ['models']

    # 指定模型和tokenizer下载保存的目录
    cache_dir = os.path.join(root_path, "lang_model")
    # 加载 tokenizer 和模型
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en", cache_dir=cache_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-zh-en", cache_dir=cache_dir)


def translate_zh_to_en(text):
    global tokenizer
    global model
    print(f"开始翻译:{text}")
    # 对输入的中文进行编码
    encoded_text = tokenizer.encode(text, return_tensors="pt")

    # 使用模型进行翻译
    translated_tokens = model.generate(encoded_text, max_length=512)

    # 将翻译后的 tokens 解码为英文文本
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    print(f"翻译成功：{translated_text}")
    return translated_text



