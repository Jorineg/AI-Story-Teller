# story visibilty options: public, unlised, private
def check_story_access(story, session):
    if story["visibility"] != "private":
        return True
    if not "user" in session:
        return False
    if story["user"]["email"] == session["user"]["email"]:
        return True
    return False


def check_story_owner(story, session):
    if not "user" in session:
        return False
    if story["user"]["email"] == session["user"]["email"]:
        return True
    return False


def story_is_valid(story):
    if story is None:
        return False
    if story["generation_level"] == -1:
        return False
    return True
