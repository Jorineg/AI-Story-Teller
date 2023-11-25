from src.ApiConnector import generate_image
import pytest


@pytest.mark.expensive
def test_generate_image():
    prompt = "A painting of a dog"
    generate_image(0, prompt, 1)
