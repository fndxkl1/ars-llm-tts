import edge_tts
import asyncio
import os
import uuid

class VoiceSynthesizer:
    def __init__(self, voice="zh-CN-XiaoyiNeural"):
        self.voice = voice
    
    async def synthesize(self, text):
        # 生成唯一文件名，避免冲突
        filename = f"response_{uuid.uuid4().hex}.mp3"
        output_file = os.path.join("output", filename)
        
        # 确保输出目录存在
        os.makedirs("output", exist_ok=True)
        
        # 使用上下文管理器确保资源释放
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_file)
        
        
        return output_file
        os.remove(output_file)
