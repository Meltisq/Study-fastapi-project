from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///tasks.db")

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# def create_table():
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS tasks (
#         id INTEGER PRIMARY KEY,
#         title TEXT NOT NULL,
#         priority INTEGER,
#         is_completed INTEGER
#     ) 
#     """)
#     connection.commit()
    
    
# def get_tasks():
#     cursor.execute("SELECT * FROM tasks")
#     return cursor.fetchall()
    
    
# def add_task(title, priority, is_completed):
#     cursor.execute("""
#         INSERT OR IGNORE INTO tasks(title, priority, is_completed)
#         VALUES(?, ?, ?)
#     """, (title, priority, is_completed))
    
#     connection.commit()


# def update_task(title, priority, is_completed, task_id):
#     cursor.execute("""
#         UPDATE tasks
#         SET title = ?, priority = ?, is_completed = ?
#         WHERE id = ?
#     """, (title, priority, is_completed, task_id))


# def delete_task(task_id):
#     cursor.execute("""
#         DELETE FROM tasks
#         WHERE id = ?          
#     """, (task_id,))