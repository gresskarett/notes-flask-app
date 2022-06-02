from operator import mod
from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import current_user
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from requests import delete
import sqlalchemy
# from sqlalchemy import insert, update, select, where, delete as sqlalchemy_delete
from . import models, db
import json


views = Blueprint('views', __name__)


@views.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # запись данных из html формы note в переменную note
        note = request.form.get("note")
        
        # проверка, вошел ли пользователь в аккаунт
        try: user_id = current_user.id
        except AttributeError: user_id = None
            
        
        if user_id is None:
            flash(message="Нужно войти в аккаунт", category="error")
        elif len(note) < 1:
            flash(message="Поле заметки не заполнено", category="error")
        else:
            new_note = models.Note(text=note, user_id=user_id)
            
            db.session.add(new_note)
            db.session.commit()
            
            flash(message="Заметка добавлена", category="success")
    
    return render_template("index.html", user=current_user)


@views.route("/edit-note", methods=["FETCH"])
def edit_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = models.Note.query.get(noteId)
    
    if (note) and (note.user_id == current_user.id):
        
        query = f'''UPDATE Note SET text = 'test' WHERE id = '{noteId}'
        '''
        
        query = update(models.Note).where(models.Note.id == noteId).values(text = "test123").\
            execution_options(synchronize_session="fetch")
        
        db.session.execute(query)
        # db.session.delete(note)
        db.session.commit()
    
    flash(message="Заметка изменена", category="success")
    
    return jsonify({})

@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = models.Note.query.get(noteId)
    
    if (note) and (note.user_id == current_user.id):
        db.session.delete(note)
        db.session.commit()
    
    flash(message="Заметка удалена", category="success")
    
    return jsonify({})
