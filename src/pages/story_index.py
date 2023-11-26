from flask import render_template, session, redirect, url_for
from Storage import get_user_credit
from Storage import find_stored_story_by_hash_id
from AccessControl import check_story_access, story_is_valid, check_story_owner
from config import DISPLAY_DATE_FORMAT, STORAGE_DATE_FORMAT
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def story_index_page(hash_id):
    story = find_stored_story_by_hash_id(hash_id)
    logger.debug(f"story_index_page: story={story}")
    if story is None or not check_story_access(story, session):
        session["toast"] = {
            "title": "Story not found",
            "message": "The story you are looking for does not exist.",
        }
        return redirect(url_for("index"))

    if story["generation_level"] == 0:
        return render_template(
            "loading_story.html",
            user=session.get("user"),
            credits=get_user_credit(session),
        )

    story_data = {
        "title": story["title"] if "title" in story else story["query"],
        "hash_id": story["hash_id"],
        "views": story["views"],
        "date": datetime.strptime(story["date"], STORAGE_DATE_FORMAT).strftime(
            DISPLAY_DATE_FORMAT
        ),
        "summary": story["summary"] if "summary" in story else "",
        # use the first image because the thumbnail is too small
        "thumbnail": url_for("stories", filename=f"{story['id']}/images/1.png"),
        "prompt": story["query"],
    }
    if check_story_owner(story, session):
        story_data["allow_edit"] = True
        story_data["visibility"] = story["visibility"]
    return render_template(
        "story_index.html",
        user=session.get("user"),
        credits=get_user_credit(session),
        story=story_data,
    )
