from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    location = db.Column(db.String(100))
    category = db.Column(db.String(50))
    people = db.Column(db.Integer)       # Nuevo campo
    duration = db.Column(db.Integer)     # Nuevo campo (minutos)

@app.route('/')
def index():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    people = request.args.get('people', '')
    duration = request.args.get('duration', '')

    query = Plan.query

    if search:
        query = query.filter(
            or_(
                Plan.title.ilike(f'%{search}%'),
                Plan.description.ilike(f'%{search}%'),
                Plan.location.ilike(f'%{search}%')
            )
        )
    if category:
        query = query.filter_by(category=category)
    if people:
        query = query.filter_by(people=int(people))
    if duration:
        query = query.filter_by(duration=int(duration))

    plans = query.all()
    return render_template('index.html', plans=plans, search=search, category=category, people=people, duration=duration)

@app.route('/create', methods=['GET', 'POST'])
def create_plan():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        category = request.form['category']
        people = int(request.form['people'])
        duration = int(request.form['duration'])

        new_plan = Plan(
            title=title,
            description=description,
            location=location,
            category=category,
            people=people,
            duration=duration
        )
        db.session.add(new_plan)
        db.session.commit()
        return redirect('/')
    return render_template('create_plan.html')

@app.route('/random')
def random_plan():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    people = request.args.get('people', type=int)
    duration = request.args.get('duration', type=int)

    query = Plan.query

    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(
            or_(
                Plan.title.ilike(f'%{search}%'),
                Plan.description.ilike(f'%{search}%'),
                Plan.location.ilike(f'%{search}%')
            )
        )
    if people is not None:
        query = query.filter_by(people=people)
    if duration is not None:
        query = query.filter_by(duration=duration)

    plans = query.all()

    if not plans:
        return render_template('random_plan.html', plan=None, category=category, search=search, people=people, duration=duration)

    plan = random.choice(plans)
    return render_template('random_plan.html', plan=plan, category=category, search=search, people=people, duration=duration)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # 🔹 Crear nueva BBDD
    app.run(debug=True)
