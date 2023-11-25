import logging
from colorlog import ColoredFormatter
import os
from dotenv import load_dotenv
from config import ROOT_PATH
import datetime
import yaml
import logging

logger = logging.getLogger(__name__)


def setup_logging():
    load_dotenv()
    console_log_level = os.getenv("CONSOLE_LOG_LEVEL", "INFO")
    file_log_level = os.getenv("FILE_LOG_LEVEL", "DEBUG")

    # format: [[time]] color [level] reset color [function]:[line] [message]
    console_formatter = ColoredFormatter(
        "[%(asctime)s] %(log_color)s%(levelname)-8s%(reset)s %(funcName)-8s:%(lineno)-3d %(message)s",
        datefmt="%H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )

    # format: [[datetime]] [level] [module] [function]:[line] [message]
    file_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(module)-20s %(funcName)-20s:%(lineno)-3d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(console_log_level)

    file_handler = logging.FileHandler(f"{ROOT_PATH}/logs/log.txt")
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(file_log_level)

    logger = logging.getLogger()
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger


gpt_logs = {}
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
gpt_log_name = f"{ROOT_PATH}/logs/gpt_log_{timestamp}.yaml"


def write_gpt_logs():
    try:
        with open(gpt_log_name, "w") as f:
            yaml.dump(gpt_logs, f)
            f.flush()
    except:
        logger.warning("failed to write log")


def create_gpt_log(prompt_name, prompt, model_input, params):
    identifier = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")

    while identifier in gpt_logs:
        identifier = identifier[:-1] + str(int(identifier[-1]) + 1)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    gpt_log = {
        "identifier": identifier,
        "prompt_name": prompt_name,
        "prompt": prompt,
        "model_input": model_input,
        "params": params,
        "timestamp_started": timestamp,
    }

    gpt_logs[identifier] = gpt_log
    write_gpt_logs()
    return identifier


def add_gpt_log_response(identifier, response):
    if identifier not in gpt_logs:
        raise RuntimeError("identifier does not exist")

    if "response" not in gpt_logs[identifier]:
        gpt_logs[identifier]["response"] = ""

    gpt_logs[identifier]["response"] += response
    write_gpt_logs()


def complete_gpt_log(identifier):
    if identifier not in gpt_logs:
        raise RuntimeError("identifier does not exist")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    gpt_logs[identifier]["timestamp_completed"] = timestamp
