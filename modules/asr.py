import os
from funasr import AutoModel
from modelscope import snapshot_download

class SpeechRecognizer:
    def __init__(self, device="cuda"):
        model_dir = snapshot_download(
            'iic/SenseVoiceSmall',
            cache_dir="models/SenseVoiceSmall"
        )
        self.model = AutoModel(
            model=model_dir,
            trust_remote_code=True,
            vad_model="fsmn-vad",
            vad_kwargs={"max_single_segment_time": 30000},
            device=device,
            batch_size_s=60
        )

    def transcribe(self, audio_path):
        res = self.model.generate(
            input=audio_path,
            language="auto",
            use_itn=True
        )
        return res[0]["text"] if res else ""