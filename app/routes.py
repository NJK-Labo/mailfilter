from flask import current_app as app
from flask import render_template


@app.route("/")
def index() -> str:
    """トップ画面"""
    return render_template("index.html")


@app.route("/contact-emails")
def list_contact_emails() -> str:
    """問い合わせメール一覧画面"""
    return render_template("list_contact_emails.html")


@app.route("/job-emails")
def list_job_emails() -> str:
    """求人関係メール一覧画面"""
    return render_template("list_job_emails.html")
