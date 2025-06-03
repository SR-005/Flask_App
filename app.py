from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
#setup database URL
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///database.db"
#Declaring Cursor for the Database
db=SQLAlchemy(app)

#initializing table for Our database 
class Task(db.Model):                                   
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(100), nullable=False)
    complete=db.Column(db.Integer, default=0)
    created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"

#index is the main page
@app.route("/",methods=["POST","GET"])
def index():
    #Adding a Task
    if request.method=="POST":
        currenttask=request.form['content']
        newtask=Task(content=currenttask)
        try:
            db.session.add(newtask)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR {e}")
            return f"ERROR {e}"
    #Current Task
    else:
        tasks=Task.query.order_by(Task.created).all()    #query to display all of the data in table orderded by date
        return render_template('index.html', tasks=tasks)
    
#Deletion Functionality
@app.route("/delete/<int:id>")
def delete(id:int):
    deletetask=Task.query.get_or_404(id)
    try:
        db.session.delete(deletetask)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error {e}"

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id:int):
    task=Task.query.get_or_404(id)
    if request.method=="POST":
        task.content = request.form["content"]
        try: 
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error {e}"
    else:
        return render_template("edit.html", task=task)
    
#to display the app in web
if __name__ in "__main__":
    with app.app_context():
        db.create_all()       #to create database file in instance folder

    app.run(debug=True) 