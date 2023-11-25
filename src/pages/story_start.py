from flask import render_template, session, redirect, url_for
from Storage import (
    find_stored_story_by_hash_id,
    update_stored_story,
    get_user_credit,
)
from routes.next_image_sound import next_image_sound_route


def start_story_page(hash_id):
    story = find_stored_story_by_hash_id(hash_id)

    if story is None or (
        story["visibility"] == "private"
        and (
            "user" not in session or story["user"]["email"] != session["user"]["email"]
        )
    ):
        session["toast"] = {
            "title": "Story not found",
            "message": "The story you are looking for does not exist.",
        }
        return redirect(url_for("index"))

    if story["generation_level"] == -1:
        session["toast"] = {
            "title": "Content filter triggered",
            "message": "Your query seems to contain inappropriate content. Please try again.",
        }
        return redirect(url_for("index"))

    if story["generation_level"] == 0:
        return render_template(
            "loading_story.html",
            user=session.get("user"),
            credits=get_user_credit(session),
        )

    story["views"] += 1
    update_stored_story(story)
    session["view_id"] = 0
    session["story"] = story
    return next_image_sound_route()
