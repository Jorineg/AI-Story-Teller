from flask import render_template, session, redirect, url_for
from Storage import get_all_stories, get_user_credit
from AccessControl import check_story_access, story_is_valid
from datetime import datetime
from config import DISPLAY_DATE_FORMAT, STORAGE_DATE_FORMAT


def my_stories_page():
    if not "user" in session:
        session["toast"] = {
            "title": "Not logged in",
            "message": "You need to be logged in to view your stories.",
        }
        return redirect(url_for("index"))

    stories = []
    for story in get_all_stories():
        if story_is_valid(story) and story["user"]["email"] == session["user"]["email"]:
            story_data = {
                "title": story["title"] if "title" in story else story["query"],
                "hash_id": story["hash_id"],
                "views": story["views"],
                "date": datetime.strptime(story["date"], STORAGE_DATE_FORMAT).strftime(
                    DISPLAY_DATE_FORMAT
                ),
                "thumbnail": url_for(
                    "stories", filename=f"{story['id']}/thumbnail.png"
                ),
            }
            stories.append(story_data)
    # sort by date
    stories.sort(key=lambda x: x["date"], reverse=True)
    return render_template(
        "collection.html",
        user=session.get("user"),
        credits=get_user_credit(session),
        stories=stories,
    )


def public_stories_page():
    stories = []
    for story in get_all_stories():
        if story_is_valid(story) and story["visibility"] == "public":
            story_data = {
                "title": story["title"] if "title" in story else story["query"],
                "hash_id": story["hash_id"],
                "views": story["views"],
                "date": datetime.strptime(story["date"], STORAGE_DATE_FORMAT).strftime(
                    DISPLAY_DATE_FORMAT
                ),
                "thumbnail": url_for(
                    "stories", filename=f"{story['id']}/thumbnail.png"
                ),
            }
            stories.append(story_data)
    # sort by views
    stories.sort(key=lambda x: x["views"], reverse=True)
    return render_template(
        "collection.html",
        user=session.get("user"),
        credits=get_user_credit(session),
        stories=stories,
    )
