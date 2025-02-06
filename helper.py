# HELPER FUNCTIONS NOT RELATED TO DB

from flask import session, abort

def require_login():
    if "user_id" not in session:
        abort(403)