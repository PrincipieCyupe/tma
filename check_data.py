from app import app, db, ToDo 

with app.app_context():
    tasks = ToDo.query.all()
    for task in tasks:
        print(f"ID: {task.id}, Content: {task.content}, Created: {task.Date_Created}")
