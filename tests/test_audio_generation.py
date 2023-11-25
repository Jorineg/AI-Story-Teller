import pytest
from src.ApiConnector import generate_audio
from pathlib import Path


@pytest.mark.expensive
def test_audio_gen():
    return
    generate_audio(0, "This is a test.", 1)
    assert Path("../stories/1/sounds/0.mp3").exists()
