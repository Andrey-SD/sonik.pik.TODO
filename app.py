from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(180), nullable=False)
    status = db.Column(db.String(50), default='false', nullable=False)

    def __repr__(self):
        return f'<Task {self.id}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['GET'])
def add_task():
    task_content = request.args.get('task')
    if task_content:
        task = Task(content=task_content)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    return 'Error: Task content not provided', 400

@app.route('/delete_task/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_status/<int:task_id>', methods=['GET'])
def update_status(task_id):
    status = request.args.get('status')
    
    task = Task.query.get(task_id)
    
    if task:
        task.status = status 
        db.session.commit() 
    return redirect(url_for('index'))

@app.route('/update_task/<int:task_id>', methods=['GET'])
def update_task(task_id):
    task_text = request.args.get('task')
    
    task = Task.query.get(task_id)
    
    if task and task_text:
        task.content = task_text 
        db.session.commit()  
    
   
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
