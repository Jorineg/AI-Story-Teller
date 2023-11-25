from flask import jsonify, session, abort, request
from Storage import find_stored_story_by_hash_id, update_stored_story
from AccessControl import check_story_owner, story_is_valid


def edit_access_route(hash_id):
    story = find_stored_story_by_hash_id(hash_id)
    if not story_is_valid(story) or not check_story_owner(story, session):
        abort(404)
    access_setting = request.get_json()
    story["visibility"] = access_setting["visibility"]
    update_stored_story(story)
    return jsonify({"success": True, "message": "Access setting updated"})
