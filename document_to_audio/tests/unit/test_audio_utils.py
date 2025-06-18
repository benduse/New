"""
Unit tests for audio utilities.
"""
import os
from document_to_audio.src.utils import audio_utils

def test_convert_text_to_audio(temp_dir, sample_text):
    """Test text to audio conversion"""
    output_path = os.path.join(temp_dir, "test_output.mp3")
    
    # Test conversion
    result_path = audio_utils.convert_text_to_audio(sample_text, output_path)
    
    # Verify file exists and has content
    assert os.path.exists(result_path)
    assert os.path.getsize(result_path) > 0
    
    # Test with different language
    output_path_es = os.path.join(temp_dir, "test_output_es.mp3")
    result_path_es = audio_utils.convert_text_to_audio(sample_text, output_path_es, language='es')
    
    # Verify Spanish audio file
    assert os.path.exists(result_path_es)
    assert os.path.getsize(result_path_es) > 0
    # Files should be different due to different languages
    assert os.path.getsize(result_path) != os.path.getsize(result_path_es)
