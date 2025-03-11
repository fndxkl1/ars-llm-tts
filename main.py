import os
import time
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import asyncio
from pynput import keyboard
import pygame
from modules.asr import SpeechRecognizer
from modules.llm import ChatAssistant
from modules.tts import VoiceSynthesizer
import torch

class VoiceAssistant:
    def __init__(self):
        # 初始化音频系统
        pygame.mixer.init()
        
        # 加载模型
        self.recognizer = SpeechRecognizer(
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
        self.assistant = ChatAssistant()
        self.tts = VoiceSynthesizer()
        
        # 录音参数
        self.sample_rate = 16000
        self.is_recording = False
        self.audio_data = []
        
        # 键盘监听
        self.listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.listener.start()

    def _on_key_press(self, key):
        """按下回车开始录音"""
        if key == keyboard.Key.enter and not self.is_recording:
            self._start_recording()

    def _on_key_release(self, key):
        """松开回车停止录音"""
        if key == keyboard.Key.enter and self.is_recording:
            self._stop_recording()

    def _start_recording(self):
        """启动录音"""
        self.is_recording = True
        self.audio_data = []
        print("\n🎙️ 录音中...（松开回车结束）")
        
        # 设置音频流
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=self._audio_callback
        )
        self.stream.start()

    def _audio_callback(self, indata, frames, time, status):
        """实时音频采集"""
        if self.is_recording:
            self.audio_data.append(indata.copy())

    def _stop_recording(self):
        """停止录音并处理"""
        self.stream.stop()
        self.is_recording = False
        print("🔄 处理中...")
        
        try:
            # 保存临时文件
            audio = np.concatenate(self.audio_data, axis=0)
            temp_file = "temp.wav"
            write(temp_file, self.sample_rate, audio)
            
            # 语音识别
            text = self.recognizer.transcribe(temp_file)
            print(f"\n🔊 识别结果：{text}")
            
            if text:
                # 生成回复
                response = self.assistant.generate_response(text)
                print(f"💡 生成回复：{response}")
                
                # 语音合成
                audio_file = asyncio.run(self.tts.synthesize(response))
                print(f"✅ 合成文件：{audio_file}")
                
                # 后台播放
                self._play_audio(audio_file)
        finally:
            # 清理临时文件
            if os.path.exists(temp_file):
                os.remove(temp_file)

    @staticmethod
    def _play_audio(file_path):
        """后台静默播放"""
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception as e:
            print(f"❌ 播放失败：{str(e)}")


if __name__ == "__main__": 
    assistant = VoiceAssistant()
    print("="*50)
    print("🗣️ 语音交互系统（按住回车录音，松开自动处理）")
    print("="*50)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n🛑 系统已安全退出")