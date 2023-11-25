import random
import time
from JsonSchemas import (
    baseline_schema,
    character_details_schema,
    validate_object,
)
from JsonParser import parse_json
from pathlib import Path

root_path = Path(__file__).parent.parent


def validate_query(query):
    time.sleep(random.random() * 2)
    return "y"
    if random.random() < 0.5:
        return "n"
    else:
        return "y"


def write_baseline(incremental, ready_to_start, query):
    time.sleep(2 + random.random() * 2)
    baseline = """
        {
        "title": "Journey of Aurora and Seraphim: The Cosmic Odyssey",
        "language": "English",
        "place": "Universe, aboard the spaceship Nebula",
        "time": "The Space Age",
        "summary": "Two unlikely companions, Aurora, a timeless fairy from the enchanted forests of Earth, and Seraphim, a 13-year-old robot operating the spaceship Nebula, find themselves on an extraordinary journey across the cosmos. Together, they navigate space-time conundrums, battle dark forces, and unravel cosmic mysteries. Can the magic of a fairy and the logic of a young robot save the universe from impending doom? Join them on a quest filled with friendship, adventure, and the wonders of the boundless universe.",
        "image_style": "anime",
        "narrator": {
            "person": "third",
            "type": "omniscient",
            "name": ""
        },
        "characters": [
            {
            "name": "Aurora",
            "species": "mythical",
            "type": "fairy",
            "age": "timeless",
            "gender": "female",
            "party": "good"
            },
            {
            "name": "Seraphim",
            "species": "robot",
            "type": "humanoid",
            "age": "13 earth years",
            "gender": "",
            "party": "neutral"
            }
        ],
        "objects": [
            {
            "name": "Nebula",
            "description": "Nebula is a state-of-the-art spaceship crafted from indestructible interstellar alloys. It boasts the latest Milky-way map and multi-galactic jumping capability, serving as the primary mode of transportation on their cosmic journey."
            },
            {
            "name": "Aurora's Magic Wand",
            "description": "Aurora's Magic Wand is an elegant, slender wand adorned with stardust and rare gemstones. It plays a pivotal role throughout their cosmic adventure, enabling Aurora to cast her spells and magic."
            }
        ]
        }
    """
    baseline_obj = parse_json(baseline)
    validate_object(baseline_obj, baseline_schema)
    for character in baseline_obj["characters"]:
        time.sleep(1 + random.random())
        incremental(character)
    time.sleep(random.random())
    return baseline_obj


def generate_character_details(baseline, character_infos):
    time.sleep(1 + random.random())
    name = character_infos["name"]
    result = """
    {
        "height": "10 cm",
        "main colors": [
            "pastel pink",
            "lavender",
            "silver"
        ],
        "skin": {
            "color": "translucent",
            "texture": "ethereal"
        },
        "properties": [
            "Long, flowing hair in shades of pastel pink and lavender",
            "Sparkling wings made of delicate, shimmering silver filaments",
            "Eyes that glow with a soft, luminescent light",
            "Gentle, ethereal aura surrounding her",
            "Wearing a flowing, iridescent dress in shades of pink and lavender",
            "Carrying a crystal wand with intricate engravings",
            "Adorned with a crown made of intricately woven flowers",
            "Glistening, silver bracelets and anklets",
            "Small, elegant silver tiara on her forehead",
            "Markings of magical symbols glowing on her skin",
            "Bare feet with a soft glow emanating from them",
            "Radiant smile that lights up her face",
            "Graceful and weightless movement",
            "Leaves a trail of twinkling stardust as she moves",
            "A soft, melodic voice that sounds like the tinkling of bells"
        ]
    }
    """
    character_details = parse_json(result)
    validate_object(character_details, character_details_schema)
    character_details["properties"].append(f"Name: {name}")
    return character_details


def generate_image_prompt(image_prompt_imput):
    time.sleep(2 + 2 * random.random())
    result = """
    masterpiece, best quality, ultra-detailed, illustration,
    1girl, solo, outdoors, camping, night, mountains, nature,
    stars, moon, tent, twin ponytails, green eyes, cheerful,
    happy, backpack, sleeping bag, camping stove, water bottle,
    mountain boots, gloves, sweater, hat, flashlight, forest,
    rocks, river, wood, smoke, shadows, contrast, clear sky,
    constellations, Milky Way, peaceful, serene, quiet, tranquil,
    remote, secluded, adventurous, exploration, escape, independence,
    survival, resourcefulness, challenge, perseverance, stamina,
    endurance, observation, intuition, adaptability, creativity,
    imagination, artistry, inspiration, beauty, awe, wonder, gratitude,
    appreciation, relaxation, enjoyment, rejuvenation, mindfulness,
    awareness, connection, harmony, balance, texture, detail, realism,
    depth, perspective, composition, color, light, shadow, reflection,
    refraction, tone, contrast, foreground, middle ground, background,
    naturalistic, figurative, representational, impressionistic,
    expressionistic, abstract, innovative, experimental, unique
    """
    return result


def generate_story(incremental, baseline):
    result = ""
    for section in range(20):
        time.sleep(5 + 5 * random.random())
        if random.random() < 0.2:
            visualization = f"""
            <text>{{
                "text": "This is a text and a number {random.randint(0, 100)}",
                "text_color": "{"red" if random.random() < 0.5 else "blue"}",
                "bg_color": "{"white" if random.random() < 0.5 else "black"}",
                "font": "times new roman"
             }}
            """
        else:
            visualization = f"""
            <image>{{
                "scenery": "The interior of the spaceship Nebula",
                "characters": ["Seraphim"],
                "objects": ["Nebula"],
                "action": "Seraphim is standing in the engine room of the spaceship Nebula, looking at the engine.",
                "mood": "excited"
            }}
            """

        text = """
        Aurora and Seraphim were on their way to the planet Earth.
        They were traveling in their spaceship Nebula.
        Aurora was sitting in the cockpit, while Seraphim was in the engine room.
        They were both excited about their upcoming adventure.
        """

        section = visualization + text
        incremental(section)
        result += section
    return result


def generate_audio(section_nr, text, story_id):
    time.sleep(5 + 5 * random.random())
    with open(f"{root_path}/stories/{story_id}/sounds/{section_nr}.mp3", "wb") as f:
        with open(
            f"{root_path}/stories/0/sounds/{random.randint(0,3)}.mp3", "rb"
        ) as dummy:
            f.write(dummy.read())
    return True


def generate_image(section_nr, image_prompt, story_id):
    time.sleep(20 + 5 * random.random())
    with open(f"{root_path}/stories/{story_id}/images/{section_nr}.png", "wb") as f:
        with open(
            f"{root_path}/stories/0/images/{random.randint(0,3)}.png", "rb"
        ) as dummy:
            f.write(dummy.read())
    return True
