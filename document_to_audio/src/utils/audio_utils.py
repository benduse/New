"""
Audio conversion utilities.
"""
from gtts import gTTS

def convert_text_to_audio(text, output_path, language='en'):
    """Convert text to audio using gTTS"""
    tts = gTTS(text=text, lang=language)
    tts.save(output_path)
    return output_path
