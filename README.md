# ars-llm-tts
简单的asr-llm-tts
目录结构：
asr-llm-tts/
├── models/                 # 预训练模型或自定义模型文件存放，目录代码会自动下载相关模型
├── modules/                # 核心功能模块
│   ├── __init__.py         # 模块初始化文件
│   ├── asr.py              # 自动语音识别（ASR）模块
│   ├── llm.py              # 大型语言模型（LLM）交互模块
│   └── tts.py              # 文本到语音（TTS）合成模块
├── output/                 # 输出文件目录
├── temp/                   # 临时文件目录（存储中间处理数据）
├── main.py                 # 主入口脚本（协调 ASR → LLM → TTS 流水线）
├── requirements.txt        # 依赖库列表（如 torch, transformers）
