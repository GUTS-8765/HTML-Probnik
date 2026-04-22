import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, g
app = Flask(__name__)
DATABASE = 'database.db'
ALLOWED_CLOUD_TYPES = [
    'undulatus', 'mammatus', 'lenticularis',
    'asperitas', 'arcus', 'other'
]
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  
        with app.app_context():
            init_db()
    return db
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                cloud_type TEXT NOT NULL,
                observer TEXT NOT NULL,
                observed_at TEXT NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False, commit=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if commit:
        get_db().commit()
    return (rv[0] if rv else None) if one else rv
@app.route('/')
def index():
    cloud_filter = request.args.get('type', '').strip()
    if cloud_filter and cloud_filter in ALLOWED_CLOUD_TYPES:
        observations = query_db(
            'SELECT * FROM observations WHERE cloud_type = ? ORDER BY observed_at DESC',
            [cloud_filter]
        )
    else:
        observations = query_db('SELECT * FROM observations ORDER BY observed_at DESC')
    return render_template('index.html',
                           observations=observations,
                           cloud_types=ALLOWED_CLOUD_TYPES,
                           current_filter=cloud_filter)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        location = request.form.get('location', '').strip()
        cloud_type = request.form.get('cloud_type', '').strip()
        observer = request.form.get('observer', '').strip()
        observed_at = request.form.get('observed_at', '').strip()
        description = request.form.get('description', '').strip()
        errors = []
        if not location:
            errors.append('Место наблюдения обязательно.')
        if not cloud_type or cloud_type not in ALLOWED_CLOUD_TYPES:
            errors.append('Выберите допустимый тип облака.')
        if not observer:
            errors.append('Имя наблюдателя обязательно.')
        if not observed_at:
            errors.append('Дата и время наблюдения обязательны.')
        else:
            try:
                datetime.fromisoformat(observed_at)
            except ValueError:
                errors.append('Неверный формат даты и времени. Используйте ГГГГ-ММ-ДДTЧЧ:ММ.')
        if errors:
            return render_template('add.html',
                                   errors=errors,
                                   form_data=request.form,
                                   cloud_types=ALLOWED_CLOUD_TYPES)
        query_db('''
            INSERT INTO observations (location, cloud_type, observer, observed_at, description)
            VALUES (?, ?, ?, ?, ?)
        ''', [location, cloud_type, observer, observed_at, description])
        return redirect(url_for('index'))
    return render_template('add.html', cloud_types=ALLOWED_CLOUD_TYPES)
if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        with app.app_context():
            init_db()
    app.run(debug=True, port=8080)