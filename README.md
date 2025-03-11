# ASR-LLM-TTS 智能对话系统

一个集成了语音识别(ASR)、大语言模型(LLM)和语音合成(TTS)的智能对话系统。

## 项目介绍

本项目使用 Qwen2.5-0.5B-Instruct 作为对话模型，实现了一个能够进行语音交互的AI助手。系统将语音输入转换为文本，通过大语言模型处理后生成回答，并将回答转换为语音输出，实现完整的语音对话流程。

## 目录结构

```plaintext
ars-llm-tts/
├── modules/
│   ├── __init__.py
│   ├── llm.py          # 大语言模型模块
│   ├── asr.py          # 语音识别模块
│   └── tts.py          # 语音合成模块
├── models/             # 模型存储目录
│   └── Qwen2.5-0.5B-Instruct/
├── requirements.txt    # 项目依赖
└── main.py            # 主程序入口
```
