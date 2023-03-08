from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, title, completed):
        self.title = title
        self.completed = completed

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = ToDo(title= title, completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect('/')

@app.route('/done/<int:todo_id>')
def done(todo_id):
    todo = ToDo.query.filter_by(id = todo_id).first()
    todo.completed = True
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = ToDo.query.filter_by(id = todo_id).first()
    db.session.delete(todo)
    db.session.commit() 
    return redirect('/')   

@app.route('/')
def main():
    ToDo_list = ToDo.query.all()
    return render_template('main.html', todo_list = ToDo_list)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    