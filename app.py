from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3
from adoption import read_adoptable_animals, write_adoptable_animal
from lost_and_found import read_lost_and_found_animals, write_lost_and_found_animal,add_lost_and_found_animal  # Add this line
from forms import LoginForm
from report_abuse import read_abuse_reports, add_abuse_report
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
import sqlite3
# SQLite database initialization
conn = sqlite3.connect('AnimalsP.db')  # Provide the correct database name
cursor = conn.cursor()

# Create the User table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Add some sample users
# cursor.execute("INSERT INTO User (username, password) VALUES ('maamon', 'password123')")
# cursor.execute("INSERT INTO User (username, password) VALUES ('user3', 'password3')")

# Commit the changes and close the connection
conn.commit()
conn.close()

from flask import render_template

@app.route('/view_users')
def view_users():
    conn = sqlite3.connect('AnimalsP.db')  # Provide the correct database name
    cursor = conn.cursor()

    # Fetch all users from the User table
    cursor.execute('SELECT * FROM User')
    users = cursor.fetchall()

    conn.close()

    return render_template('view_users.html', users=users)


# ...

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if request.method == 'GET':
        # Redirect to login.html for the GET method
        return render_template('login.html', form=form)
    elif request.method == 'POST' and form.validate_on_submit():
        conn = sqlite3.connect('AnimalsP.db')  # Provide the correct database name
        cursor = conn.cursor()

        # Check if the entered username and password match a user in the database
        cursor.execute('SELECT * FROM User WHERE username=? AND password=?',
                       (form.username.data, form.password.data))
        user = cursor.fetchone()

        conn.close()

        if user:
            flash('Login successful', 'success')
            return redirect(url_for('menu', username=form.username.data))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)

# ...



@app.route('/adopt', methods=['GET', 'POST'])
def adopt():
    if request.method == 'GET':
        animals = read_adoptable_animals()
        return render_template('adopt.html', animals=animals)
    elif request.method == 'POST':
        choice = request.form.get('choice')
        if choice == 'put_for_adoption':
            return redirect(url_for('put_for_adoption'))
        elif choice == 'adopt':
            new_animal = {
                'name': request.form.get('name'),
                'species': request.form.get('species'),
                'age': request.form.get('age'),
                'description': request.form.get('description'),
                'contact': request.form.get('contact')
            }
            write_adoptable_animal(new_animal)
            return redirect(url_for('adopt'))
@app.route('/menu')
def menu():
    username = request.args.get('username')
    return render_template('menu.html', username=username)


@app.route('/put_for_adoption', methods=['GET', 'POST'])
def put_for_adoption():
    if request.method == 'GET':
        return render_template('put_for_adoption.html')
    elif request.method == 'POST':
        new_animal = {
            'name': request.form.get('name'),
            'species': request.form.get('species'),
            'age': request.form.get('age'),
            'description': request.form.get('description'),
            'contact': request.form.get('contact')
        }
        write_adoptable_animal(new_animal)
        flash("Animal put up for adoption successfully", "success")
        return redirect(url_for('put_for_adoption'))


@app.route('/report_abuse', methods=['GET', 'POST'])
def report_abuse():
    if request.method == 'GET':
        return render_template('report_abuse.html')
    elif request.method == 'POST':
        abuse_report = {
            'abuse_type': request.form.get('abuse_type'),
            'description': request.form.get('description')
        }
        add_abuse_report(abuse_report)
        flash("Animal abuse reported successfully", "success")
        return redirect(url_for('report_abuse'))

@app.route('/lost_and_found', methods=['GET', 'POST'])
def lost_and_found():
    if request.method == 'GET':
        lfanimals = read_lost_and_found_animals()
        return render_template('lost_and_found.html', lfanimals=lfanimals)
    elif request.method == 'POST':
        new_animal = {
            'name': request.form.get('name'),
            'species': request.form.get('species'),
            'description': request.form.get('description'),
            'contact': request.form.get('contact')
        }
        add_lost_and_found_animal(new_animal)
        flash("Lost and found information submitted successfully", "success")
        return redirect(url_for('lost_and_found'))

if __name__ == '__main__':
    app.run(debug=True)
