import sys
import os
from sqlmodel import Session, create_engine, select
from uuid import UUID

sys.path.insert(0, 'src')
from core.config import settings
from models.task import Task

engine = create_engine(settings.DATABASE_URL)

def list_all_tasks():
    with Session(engine) as session:
        stmt = select(Task).order_by(Task.created_at.desc())
        tasks = session.exec(stmt).all()
        
        print(f"{'ID':<40} | {'Title':<20} | {'Completed':<10} | {'Created At'}")
        print("-" * 90)
        for task in tasks:
            print(f"{str(task.id):<40} | {task.title:<20} | {str(task.is_completed):<10} | {task.created_at}")

if __name__ == "__main__":
    list_all_tasks()
