from flask import redirect, render_template, request, session
from functools import wraps

def login_demanding(f): #name de funtion.
    @wraps(f) 
    def decorated(*args, **kwargs):
        if session.get("username") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated