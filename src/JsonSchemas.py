from jsonschema import validate, ValidationError
import logging

logger = logging.getLogger(__name__)


def validate_object(obj, schema, raise_exception=True):
    try:
        validate(obj, schema)
    except ValidationError as e:
        logger.exception("Validation error")
        logger.info("Decoded json object:")
        logger.info(obj)
        if raise_exception:
            raise RuntimeError("Returned JSON does not match expected format")
        return False
    return obj


baseline_schema = {
    "type": "object",
    "properties": {
        "language": {"type": "string"},
        "place": {"type": "string"},
        "time": {"type": "string"},
        "title": {"type": "string"},
        "title_font_color": {"type": "string"},
        "title_font_family": {"type": "string"},
        "title_background_color": {"type": "string"},
        "image_style": {"type": "string"},
        "narrator": {
            "type": "object",
            "properties": {
                "person": {"type": "string"},
                "type": {"type": "string"},
                "name": {"type": "string"},
            },
            "required": ["person", "type"],
        },
        "audio_narrator": {"type": "string"},
        "characters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "species": {"type": "string"},
                    "type": {"type": "string"},
                    "age": {"type": "string"},
                    "gender": {"type": "string"},
                    "party": {"type": "string"},
                },
            },
            "required": ["name", "species", "type", "age", "gender", "party"],
            "additionalProperties": False,
        },
        "objects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                },
            },
            "required": ["name", "description"],
            "additionalProperties": False,
        },
    },
    "required": [
        "title",
        "title_font_color",
        "title_font_family",
        "title_background_color",
        "language",
        "place",
        "time",
        "image_style",
        "narrator",
        "audio_narrator",
        "characters",
        "objects",
    ],
    "additionalProperties": False,
}


story_text_schema = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "text_color": {"type": "string"},
        "bg_color": {"type": "string"},
        "font": {"type": "string"},
    },
    "required": ["text", "text_color", "bg_color", "font"],
    "additionalProperties": False,
}


story_image_schema = {
    "type": "object",
    "properties": {
        "scenery": {"type": "string"},
        "characters": {"type": "array", "items": {"type": "string"}},
        "objects": {"type": "array", "items": {"type": "string"}},
        "action": {"type": "string"},
        "mood": {"type": "string"},
    },
    "required": ["scenery", "characters", "objects", "action", "mood"],
    "additionalProperties": False,
}


character_details_schema = {
    "type": "object",
    "properties": {
        "height": {"type": "string"},
        "skin": {
            "type": "object",
            "properties": {
                "color": {"type": "string"},
                "texture": {"type": "string"},
            },
            "required": ["color", "texture"],
            "additionalProperties": False,
        },
        "appearance": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["height", "skin", "appearance"],
}
