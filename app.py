from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There is issue in adding task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)
    # return render_template('index.html')
@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Todo.query.get(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There is an error to delete task'


@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = Todo.query.get(id)

    if request.method == 'POST':
        task.content = request.form['content'] 
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There is an issue to update" 
    else:
        return render_template('update.html',task=task)




@app.route('/about')
def about():
    return 'Check it again but it is still working'

if __name__ == '__main__':
    app.run(debug=True)