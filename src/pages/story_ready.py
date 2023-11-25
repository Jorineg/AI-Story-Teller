from flask import render_template, redirect, url_for, session
from Storage import find_stored_story_by_hash_id


def story_ready_page(hash_id):
    story = find_stored_story_by_hash_id(hash_id)
    if story["generation_level"] == 0:
        return redirect(url_for("story_index", hash_id=hash_id))
    if story["generation_level"] == -1:
        session["toast"] = {
            "title": "Unexpected Error",
            "message": "An unexpected error occured while generating your story. Please try again.",
        }
        if "error" in story:
            error = story["error"]["type"]
            if error == "content filter triggered":
                session["toast"] = {
                    "title": "Content filter triggered",
                    "message": "Your query seems to contain inappropriate content. Please try again.",
                }
            elif error == "generation error":
                session["toast"] = {
                    "title": "Story Generation Error",
                    "message": "An error occured while generating your story. Please try again.",
                }
        return redirect(url_for("index"))
    return render_template(
        "story_ready.html",
        user=session.get("user"),
        credits=session.get("credits", 0),
        story=story,
    )
