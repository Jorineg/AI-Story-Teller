from flask import render_template, session, url_for, redirect
from Storage import (
    find_stored_story_by_hash_id,
    get_texts_for_story,
)
import logging

logger = logging.getLogger(__name__)


def redirect_home_with_general_error():
    session["toast"] = {
        "title": "Error",
        "message": "This seems to be an error. Please try again.",
    }
    return redirect(url_for("index"))


def next_image_sound_route():
    if not "story" in session:
        return redirect_home_with_general_error()

    story_id = session["story"]["id"]
    view_id = str(session["view_id"])
    logger.debug(f"called nextimagesound for story {story_id} and view {view_id}")

    story_hash_id = session["story"]["hash_id"]
    try:
        generation_level = find_stored_story_by_hash_id(story_hash_id)[
            "generation_level"
        ]
    except:
        return "false"

    if generation_level <= session["view_id"]:
        return "false"

    text_illustrations = get_texts_for_story(story_id)
    has_sound = True
    if view_id in text_illustrations:
        img = {"text": text_illustrations[view_id]}
        if "end" in text_illustrations[view_id] and text_illustrations[view_id]["end"]:
            has_sound = False
    else:
        img = {
            "image_url": url_for("stories", filename=f"{story_id}/images/{view_id}.png")
        }
    sound = {"sound_url": None}
    if has_sound:
        sound["sound_url"] = url_for(
            "stories", filename=f"{story_id}/sounds/{view_id}.mp3"
        )

    session["view_id"] += 1
    return render_template("imagesound.html", **sound, **img)
