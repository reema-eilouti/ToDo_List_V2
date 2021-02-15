from flask import Flask, render_template, redirect, url_for, request, Blueprint, session
import sqlite3
import datetime
from functools import wraps
from to_do_tasks.db import get_db
from ..forms import EditNameForm, CreateTaskList


# define our blueprint
taskslist_bp = Blueprint('taskslist', __name__)

def login_required(function):
    @wraps(function)
    
    def check(*args, **kwargs):        

        if 'uid' in session:
            return function(*args, **kwargs)
            
        else:
            return redirect(url_for('user.login'))
            
    return check


#Task list routing
@taskslist_bp.route("/")
@login_required
def task_lists():

    # connecting to the database
    db = get_db()

    lists = db.execute("SELECT * FROM taskslist").fetchall()

    return render_template("tasks_list/tasklists.html", lists = lists)

#Edit task list routing
@taskslist_bp.route("/editname/<int:index>" , methods=["POST" , "GET"])
@login_required
def edit_tasklist_name(index):

    edit_name_form = EditNameForm()

    if edit_name_form.validate_on_submit():

        new_name = edit_name_form.new_name.data

        # connecting to the database
        db = get_db()

        db.execute(f"UPDATE taskslist SET name = '{new_name}' , last_updated = '{datetime.datetime.now()}' WHERE id = '{index}' ")
            
        db.commit()

        return redirect(url_for('taskslist.task_lists'))

    return render_template("tasks_list/edit_name.html", form = edit_name_form)

#Delete task list routing
@taskslist_bp.route("/deletetasklist/<int:index>")
@login_required
def delete_tasklist(index):

    # connecting to the database
    db = get_db()

    db.execute(f"DELETE FROM taskslist WHERE id = '{index}' ")
            
    db.commit()

    return redirect(url_for("taskslist.task_lists"))

#Create task list routing
@taskslist_bp.route("/createtasklist" , methods = ["GET","POST"])
@login_required
def create_tasklist():
    create_tasklist = CreateTaskList()

    if create_tasklist.validate_on_submit():

        name = create_tasklist.name.data

        # connecting to the database
        db = get_db()

        db.execute("INSERT INTO taskslist (name) VALUES (?);" , (name,))
            
        db.commit()

        return redirect(url_for('taskslist.task_lists'))

    return render_template("tasks_list/create_tasklist.html", form = create_tasklist )

#Sort task list routing
@taskslist_bp.route("/sort_list")
@login_required
def sort():

    # connecting to the database
    db = get_db()

    #Retrieve task list in alphabetical order
    lists = db.execute('SELECT id, name, last_updated, created_at'
        ' FROM taskslist'
        ' ORDER BY name ASC'
    ).fetchall()

    return render_template("tasks_list/tasklists.html", lists = lists)

