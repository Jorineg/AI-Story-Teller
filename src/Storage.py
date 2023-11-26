import json
import os
from pathlib import Path
from PIL import Image

root_path = Path(__file__).parent.parent


def find_stored_story_by_id(id):
    with open(f"{root_path}/stories/saved_stories.json", "r") as f:
        json_data = json.load(f)
    for story in json_data:
        if story["id"] == id:
            return story
    return None


def find_stored_story_by_hash_id(hash_id):
    with open(f"{root_path}/stories/saved_stories.json", "r") as f:
        try:
            json_data = json.load(f)
        except:
            return None
    for story in json_data:
        if story["hash_id"] == hash_id:
            return story
    return None


def update_stored_story(story):
    with open(f"{root_path}/stories/saved_stories.json", "r") as f:
        json_data = json.load(f)
    for i, s in enumerate(json_data):
        if s["hash_id"] == story["hash_id"]:
            json_data[i] = story
    with open(f"{root_path}/stories/saved_stories.json", "w") as f:
        json.dump(json_data, f, indent=4)


def store_new_story(**info):
    with open(f"{root_path}/stories/saved_stories.json", "r") as f:
        json_data = json.load(f)
    max_id = max((story["id"] for story in json_data), default=0)
    story_id = max_id + 1
    new_story_data = {"id": story_id, **info}
    json_data.append(new_story_data)
    with open(f"{root_path}/stories/saved_stories.json", "w") as f:
        json.dump(json_data, f, indent=4)
        f.flush()
        os.fsync(f)
    return new_story_data


def get_texts_for_story(id):
    with open(f"{root_path}/stories/{id}/texts.json", "r") as f:
        json_data = json.load(f)
    return json_data


# def get_allowed_users():
#     allowed_users = []
#     with open("allowed_users.txt", "r") as f:
#         for line in f:
#             allowed_users.append(line.strip())
#     return allowed_users


def store_value(session, key, value):
    session[key] = value


def load_value(session, key):
    return session.get(key)


def create_story_folder(story_id, _):
    os.mkdir(f"{root_path}/stories/{story_id}")
    os.mkdir(f"{root_path}/stories/{story_id}/images")
    os.mkdir(f"{root_path}/stories/{story_id}/sounds")
    texts_json = {}
    with open(f"{root_path}/stories/{story_id}/texts.json", "w") as f:
        json.dump(texts_json, f, indent=4)


def store_story_baseline(baseline, story_id):
    with open(f"{root_path}/stories/{story_id}/baseline.json", "w") as f:
        json.dump(baseline, f, indent=4)


def store_story(story_id, *sections):
    whole_story = "\n".join(sections)
    with open(f"{root_path}/stories/{story_id}/story.txt", "w") as f:
        f.write(whole_story)


def store_text_illustration(section_nr, text_illustration, story_id, *_):
    json_data = {}
    if os.path.exists(f"{root_path}/stories/{story_id}/texts.json"):
        with open(f"{root_path}/stories/{story_id}/texts.json", "r") as f:
            json_data = json.load(f)

    json_data[section_nr] = text_illustration
    with open(f"{root_path}/stories/{story_id}/texts.json", "w") as f:
        json.dump(json_data, f, indent=4)
    return True


def use_credit_for_user(session):
    if session is None or session.get("user") is None:
        return False
    user = session["user"]["email"]
    with open(f"{root_path}/user_credits.json", "r") as f:
        json_data = json.load(f)
        if user not in json_data:
            return False
        if json_data[user] <= 0:
            return False
        json_data[user] -= 1
    with open(f"{root_path}/user_credits.json", "w") as f:
        json.dump(json_data, f, indent=4)
        return True


def get_user_credit(session):
    if session is None or session.get("user") is None:
        return 0
    with open(f"{root_path}/user_credits.json", "r") as f:
        json_data = json.load(f)
        email = session["user"]["email"]
        if email not in json_data:
            return 0
        return json_data[email]


def store_story_ending(section_nr, story_id, _):
    end_text = {
        "text": "This is the end of the story. Press esc to exit.",
        "bg_color": "#000000",
        "text_color": "#ffffff",
        "font": "Times New Roman",
        "font_size": "30px",
        "end": True,
    }
    store_text_illustration(section_nr + 1, end_text, story_id)


# takes first image from story, scales it down and stores it as thumbnail
def store_story_thumbnail(story_id, _):
    image = Image.open(f"{root_path}/stories/{story_id}/images/1.png")
    image.thumbnail((300, 171))
    image.save(f"{root_path}/stories/{story_id}/thumbnail.png")


def get_all_stories():
    with open(f"{root_path}/stories/saved_stories.json", "r") as f:
        json_data = json.load(f)
    return json_data
