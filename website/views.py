from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=["GET", "POST"]) # Decorator
@login_required # Makes it so that the home page can only be reached once logged in
def home():
	if request.method == "POST":
		note = request.form.get('note')

		if len(note) < 1:
			flash("Note is too short.", category="error")
		else:
			new_note = Note(data=note, user_id=current_user.id)
			db.session.add(new_note)
			db.session.commit()
			flash("Note added!", category="success")

	return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=["POST"])
def delete_note():
	note = json.loads(request.data) # Takes in data from POST request
	noteId = note['noteId']         # Access noteId attribute from Python dictionary
	note = Note.query.get(noteId)
	if note:
		if note.user_id == current_user.id: # Verify that the current user is the note's owner
			db.session.delete(note)
			db.session.commit()
	
	return jsonify({})