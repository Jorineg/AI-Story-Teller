from flask import send_from_directory, session
from config import STATIC_FOLDER, STORY_FOLDER
import os
from Storage import find_stored_story_by_id


def send_static_image_with_cache(filename):
    # Check if the requested file is an image
    valid_image_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    file_extension = os.path.splitext(filename)[1]
    if file_extension in valid_image_extensions:
        # cache_timeout is in seconds, set to 1 year
        cache_timeout = 31536000
    else:
        cache_timeout = None
    # Serve the static file and apply the cache timeout
    return send_from_directory(STATIC_FOLDER, filename, cache_timeout=cache_timeout)


# first check if user has access to the file, then serve it
def send_story_data(filename):
    user_email = None
    if "user" in session:
        user_email = session["user"]["email"]
    story_id = int(filename.split("/")[0])
    story_data = find_stored_story_by_id(story_id)
    story_not_found = ("Story not found", 404)
    if story_data is None:
        return story_not_found
    if story_data["visibility"] == "private" and (
        user_email is None or story_data["user"]["email"] != user_email
    ):
        return story_not_found
    return send_from_directory(STORY_FOLDER, filename)
