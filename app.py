from flask import Flask, render_template, request, redirect,session, url_for #new1
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta

# Initialize Flask app and SQLAlchemy
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask app configuration  #new1
app.secret_key = 'hidynamic'  # Replace with a secure one!
PASSWORD = 'abhishek'  # Set your login password here

# Create the database and the Todo model
class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=5, minutes=30))

    def __repr__(self):
        return f'<Todo {self.title}>'

# Login functionality #new1
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('hello_world'))
        else:
            return render_template('login.html', error='Incorrect password')
    return render_template('login.html')

# Create the home route #new1 replaced
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)
        print(title, description)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

""" 
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)
        print(title, description)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)
     """

# About page
@app.route('/about')
def product():
    return render_template('about.html') 

# Delete todo
@app.route('/delete/<int:SNo>')
def delete(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


'''
@app.route('/delete/<int:SNo>')
def delete(SNo):
    return redirect("/")
'''

# Update todo
@app.route('/update/<int:SNo>', methods=['GET', 'POST'])
def update(SNo):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(SNo=SNo).first()
        todo.title = title  
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(SNo=SNo).first()
    return render_template('update.html', todo=todo)

#view todo
@app.route('/view/<int:SNo>')
def view(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first_or_404()
    return render_template('view.html', todo=todo)
    
#search bar
@app.route("/search")
def search():
    query = request.args.get('query')
    if not query or query.strip() == "":
        allTodo = Todo.query.all()
        return render_template('index.html', allTodo=allTodo)
    allTodo = Todo.query.filter(
        (Todo.title.contains(query)) 
    ).all()
    return render_template('index.html', allTodo=allTodo)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
