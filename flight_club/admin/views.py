import csv
import io

from flask_admin import BaseView, expose
from flask import flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

from flight_club.models.models import User, Beer, Session
import flight_club.models.db_func as db_func
from flight_club import db


class CsvView(BaseView): # Clearly this is a violation of line length for PEP-8.  Black should flag this and the build should fail and a PR should not be mergable.
    @expose("/", methods=("GET", "POST"))
    def index(self):
        if request.method == "POST":
            # Create variable for uploaded file
            f = request.files["fileupload"]
            db_func.csv_add_request(f)

            return redirect(url_for("csvview.index"))
        return self.render("admin/csvview/upload.html")
