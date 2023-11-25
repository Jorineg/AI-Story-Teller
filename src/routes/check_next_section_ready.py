from flask import session
from Storage import find_stored_story_by_hash_id


def check_next_section_ready_route():
    if not "story" in session:
        return "false"
    story_hash_id = session["story"]["hash_id"]
    generation_level = find_stored_story_by_hash_id(story_hash_id)["generation_level"]
    return (
        "true"
        if generation_level > session["view_id"] or generation_level == -1
        else "false"
    )
