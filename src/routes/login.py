from flask import redirect, url_for, request, session
import os
from google.oauth2 import id_token
from google.auth.transport import requests


def google_auth():
    token = request.form["credential"]
    if token is None:
        return "Bad Request", 400
    idinfo = id_token.verify_oauth2_token(
        token, requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
    )
    session["user"] = idinfo
    main_page = url_for("index")
    return redirect(main_page)


def session_logout():
    session.pop("user", None)
    return redirect(url_for("index"))
