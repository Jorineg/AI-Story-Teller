from flask import render_template, request, session, redirect, url_for
from Storage import get_user_credit, use_credit_for_user, store_new_story
from StoryWriter import create_new_story
from datetime import datetime
import os
from config import STORAGE_DATE_FORMAT


def index_page():
    if request.method == "POST":
        return generate()

    if "story" in session:
        session.pop("story", None)
        session.pop("view_id", None)

    toast = None
    if "toast" in session:
        toast = {
            "title": session["toast"]["title"],
            "message": session["toast"]["message"],
        }
        session.pop("toast", None)
    return render_template(
        "index.html",
        user=session.get("user"),
        credits=get_user_credit(session),
        toast=toast,
    )


def generate():
    user_logged_in = "user" in session
    user_can_create = user_logged_in and get_user_credit(session) > 0
    query = request.form["query"].replace("\n", " ").replace("\r", " ").strip()

    if user_can_create:
        info = {
            "date": datetime.now().strftime(STORAGE_DATE_FORMAT),
            "query": query,
            "user": {
                "name": session["user"]["given_name"],
                "email": session["user"]["email"],
            },
            "visibility": "public",
            "views": 0,
            "hash_id": os.urandom(12).hex(),
            "generation_level": 0,
        }
        story = store_new_story(**info)
        use_credit_for_user(session)
        create_new_story(query, story["id"])
        session["story"] = story
        session["view_id"] = 0
        return redirect(url_for("story", hash_id=story["hash_id"]))
        # return render_template(
        #     "loading_story.html",
        #     user=session.get("user"),
        #     credits=get_user_credit(session),
        # )
    else:
        toast = {
            "title": "Not enough credits" if user_logged_in else "Not logged in",
            "message": "You need to be logged in and have credits to generate a new story.",
        }
        return render_template(
            "index.html",
            user=session.get("user"),
            credits=get_user_credit(session),
            toast=toast,
        )
