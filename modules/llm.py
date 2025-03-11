from modelscope import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

class ChatAssistant:
    def __init__(self):
        
        # 模型下载
        model_dir = snapshot_download(
            "Qwen/Qwen2.5-0.5B-Instruct",
            cache_dir="models/Qwen2.5-0.5B-Instruct"
        )
        
        # 模型初始化
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_dir,
            torch_dtype="auto", #自动选择数据类型
            device_map="auto"   #自动选择设备(cpu还是GPU)
        )

    def generate_response(self, prompt):
        messages = [
            {"role": "system", "content": "你的名字叫小恐龙，温柔体贴，喜欢用网络梗回答，回答简洁"},  #定义提示词
            {"role": "user", "content": f"{prompt}（50字内回答）"}
        ]
        
        inputs = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([inputs], return_tensors="pt").to(self.model.device)
        
        outputs = self.model.generate(
            **model_inputs,
            max_new_tokens=100
        )
        return self.tokenizer.decode(outputs[0][len(model_inputs.input_ids[0]):], skip_special_tokens=True)
