from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timezone

#my App
app=Flask(__name__)
Scss(app) 


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    scheduled_time = db.Column(db.DateTime, nullable=True)    

def __repr__(self) -> str:
    return f"Task {self.id}"
    
#Home page
@app.route("/", methods=["POST", "GET"])
def index():

    #Add task
    if request.method == "POST":
        current_task = request.form['content']
        scheduled_time_str = request.form['scheduled_time']
        scheduled_time = datetime.strptime(scheduled_time_str, "%Y-%m-%dT%H:%M") if scheduled_time_str else None
        new_task = MyTask(content=current_task, scheduled_time=scheduled_time)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"

    #see current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)



#Delete
@app.route("/delete/<int:id>")
def delete(id:int):
        delete_task = MyTask.query.get_or_404(id)
        try:
            db.session.delete(delete_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"

#Edit

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        scheduled_time_str = request.form['scheduled_time']
        task.scheduled_time = datetime.strptime(scheduled_time_str, "%Y-%m-%dT%H:%M") if scheduled_time_str else None
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template("update.html", task=task)       



if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
