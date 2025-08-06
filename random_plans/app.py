from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
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

@app.route('/')
def index():
    plans = Plan.query.all()
    return render_template('index.html', plans=plans)

@app.route('/create', methods=['GET', 'POST'])
def create_plan():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        category = request.form['category']
        new_plan = Plan(title=title, description=description, location=location, category=category)
        db.session.add(new_plan)
        db.session.commit()
        return redirect('/')
    return render_template('create_plan.html')

@app.route('/random')
def random_plan():
    plans = Plan.query.all()
    if plans:
        plan = random.choice(plans)
        return render_template('random_plan.html', plan=plan)
    return "No hay planes aún."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)