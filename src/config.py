from pathlib import Path

STATIC_FOLDER = "../static"
TEMPLATE_FOLDER = "../templates"
STORY_FOLDER = "../stories"
ROOT_PATH = Path(__file__).parent.parent

# max retries for gpt requests, if the response is not in the specified format
MAX_RETRY_RESPONSE_FORMAT_FAIL = 3

DISPLAY_DATE_FORMAT = "%Y-%m-%d"
STORAGE_DATE_FORMAT = "%d/%m/%Y %H:%M:%S"

prompt_params = {
    "MIN_PARAGRAPHS": 15,
    "MAX_PARAGRAPHS": 20,
    "PARAGRAPH_WORDS": 120,
}
