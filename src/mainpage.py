from dotenv import load_dotenv

load_dotenv()

from flask import (
    Flask,
    render_template,
    session,
)
import os
from Storage import get_user_credit
from config import STATIC_FOLDER, TEMPLATE_FOLDER
from pages.home import index_page
from pages.story_collection import my_stories_page, public_stories_page
from pages.story_start import start_story_page
from pages.story_index import story_index_page
from pages.story_ready import story_ready_page
from routes.file_hosting import send_static_image_with_cache, send_story_data
from routes.next_image_sound import next_image_sound_route
from routes.login import google_auth, session_logout
from routes.check_next_section_ready import check_next_section_ready_route
from routes.access import edit_access_route
from Logging import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)
app.secret_key = os.urandom(12)


app.add_url_rule(
    f"/stories/<path:filename>",
    endpoint="stories",
    view_func=send_story_data,
)


@app.route("/static/<path:filename>")
def static_images(filename):
    return send_static_image_with_cache(filename)


@app.route("/", methods=["GET", "POST"])
def index():
    logger.debug("called index")
    return index_page()


@app.route("/google/auth", methods=["POST", "GET"])
def googleauth():
    return google_auth()


@app.route("/logout")
def logout():
    return session_logout()


@app.route("/story/<hash_id>")
def story(hash_id):
    return story_index_page(hash_id)
    # story = find_stored_story_by_hash_id(hash_id)

    # generation_level = story["generation_level"]

    # if generation_level == -1:
    #     session["toast"] = {
    #         "title": "Content filter triggered",
    #         "message": "Your query seems to contain inappropriate content. Please try again.",
    #     }
    #     return redirect(url_for("index"))

    # if generation_level == 0:
    #     return render_template(
    #         "loading_story.html",
    #         user=session.get("user"),
    #         credits=get_user_credit(session),
    #     )

    # return render_template(
    #     "start_story.html", user=session.get("user"), credits=session.get("credits", 0)
    # )


@app.route("/story/<hash_id>/ready")
def story_ready(hash_id):
    return story_ready_page(hash_id)


@app.route("/story/<hash_id>/start")
def story_start(hash_id):
    return start_story_page(hash_id)


@app.route("/publicstories")
def public_stories():
    return public_stories_page()


@app.route("/mystories")
def my_stories():
    return my_stories_page()


@app.route("/nextimagesound")
def next_image_sound():
    return next_image_sound_route()


@app.route("/checknextsectionready")
def check_next_section_ready():
    return check_next_section_ready_route()


@app.route("/story/<hash_id>/access", methods=["POST"])
def story_access(hash_id):
    return edit_access_route(hash_id)


@app.route("/about")
def about():
    return render_template(
        "about.html", user=session.get("user"), credits=get_user_credit(session)
    )


if __name__ == "__main__":
    app.run(debug=True)
