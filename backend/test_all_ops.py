import sys
import os
from uuid import UUID

sys.path.insert(0, 'src')
from models.task import Task
from models.user import User
from models.chat import Conversation, Message

from ai.mcp_server import add_task, list_tasks, search_tasks, update_task, update_task_status, delete_task

def test_all_ops():
    user_id = "00000000-0000-0000-0000-000000000001" # Mock user_id
    
    print("--- 1. Testing Add Task ---")
    new_task = add_task(user_id, "Test Agent Task", "Testing all operations", "high")
    task_id = str(new_task['id'])
    print(f"Added task: {task_id}")

    print("\n--- 2. Testing List Tasks ---")
    tasks = list_tasks(user_id)
    print(f"Found {len(tasks)} tasks")
    assert any(str(t['id']) == task_id for t in tasks)

    print("\n--- 3. Testing Update Status ---")
    res = update_task_status(task_id, True)
    print(res)
    
    # Verify status in DB
    tasks = list_tasks(user_id)
    target = next(t for t in tasks if str(t['id']) == task_id)
    print(f"Status in DB: {target['is_completed']}")
    assert target['is_completed'] == True

    print("\n--- 4. Testing Update Task (Edit) ---")
    res = update_task(task_id, title="Updated Title", priority="low")
    print(res)
    
    tasks = list_tasks(user_id)
    target = next(t for t in tasks if str(t['id']) == task_id)
    print(f"Title in DB: {target['title']}, Priority: {target['priority']}")
    assert target['title'] == "Updated Title"
    assert target['priority'] == "low"

    print("\n--- 5. Testing Delete Task ---")
    res = delete_task(task_id)
    print(res)
    
    tasks = list_tasks(user_id)
    assert not any(str(t['id']) == task_id for t in tasks)
    print("Delete verified")

    print("\n--- ALL TESTS PASSED ---")

if __name__ == "__main__":
    test_all_ops()
