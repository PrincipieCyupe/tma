from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sys
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("Error: The environment variable DATABASE_URL is not set.")
    sys.exit(1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print("Database URI resolved to:", app.config['SQLALCHEMY_DATABASE_URI'])

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    Date_Created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task: {self.id}>"

@app.route('/', methods=['POST', 'GET'])
@app.route('/home')
def home_page():

    if request.method == 'POST':
        task_content = request.form['content']
        new = ToDo(content=task_content)
        db.session.add(new)
        db.session.commit()
        return redirect('/home')
    else:
        tasks = ToDo.query.order_by(ToDo.Date_Created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    ttodel = ToDo.query.get_or_404(id)
    db.session.delete(ttodel)
    db.session.commit()

    return redirect('/')

@app.route('/update/<int:id>')
def update(id):
    ttoup = ToDo.query.get_or_404(id)
    old_delete = ttoup
    db.session.delete(old_delete)
    db.session.commit()
    return render_template('updated.html', task=ttoup)


if __name__ == "__main__":
    with app.app_context():
        print("The current working directory is:", os.getcwd())
        db.create_all()
        print("Database is succesfully created in current directory")

    app.run(debug=True, host='0.0.0.0', port=5000)