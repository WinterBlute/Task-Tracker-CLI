'''Task Tracker CLI application for Python Projects. Uses a JSON file and performs CRUD operations on lists'''

import json
import time
TASK_FILE = 'tasklist.json'
VALID_STATUSES = ('in-progress', 'done', 'to-do')

def add(task: str, task_id: int, status: str = 'to-do') -> dict:
    '''Adds a new task to the tasklist'''
    data = {
        'id': task_id,
        'task': task,
        'status': status,
        'createdAt' : time.ctime(),
        'updatedAt' : None
    }
    return data

def load_tasks() -> list:
    '''Loads the current saved list in the JSON file'''
    try:
        with open(TASK_FILE, 'r') as f:
            tasks = json.load(f)
            return tasks if isinstance(tasks, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks: list) -> None:
    '''Saves the current iteration of the list in the JSON file'''
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def next_task_id(tasks: list) -> int:
    '''Generates the next id number of tasks'''
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def update_task(tasks: list, task_id: int, new_text: str) -> bool:
    '''Update the task of a designated task id'''
    for task in tasks:
        if task["id"] == task_id:
            task["task"] = new_text
            task["updatedAT"] = time.ctime()
            return True
    return False

def delete_task(tasks: list, task_id: int) -> bool:
    '''Delete the task by its designated task id'''
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return True
    return False

def mark_task(tasks: list, status: str, task_id: int) -> bool:
    '''Changes the status of the task by its task id to any of the three valid statuses'''
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAT"] = time.ctime()
            return True
    return False
    
def main():
    '''Runs the main loop of the CLI Program'''
    current_list = load_tasks()
    
    while True:
        raw_input = input('task-cli ')
        command = raw_input.split()
        if not command:
            continue
        action = command[0].lower()
        if action == "close":
            break
        elif action == "add":
            if len(command) < 2:
                print("Please provide a task.")
                continue
            task = add(" ".join(command[1:]), next_task_id(current_list))
            current_list.append(task)
            save_tasks(current_list)
            print("Task added successfully")
        elif action == "clear":
            current_list = []
            save_tasks(current_list)
            print("Task list successfully cleared.")
        elif action == "update":
            if len(command) < 3:
                print("Incorrect formatting")
                continue
            try:
                update_id = int(command[1])
            except ValueError:
                print("id must be an integer")
                continue
            new_task = " ".join(command[2:])
            updated = update_task(current_list, update_id, new_task)
            if updated:
                save_tasks(current_list)
                print("Task has been updated")
            else:
                print("Task id not found")
        elif action == "delete":
            if len(command) < 2:
                print("Incorrect formatting")
                continue
            try:
                delete_id = int(command[1])
            except ValueError:
                print("id must be an integer")
                continue
            deleted = delete_task(current_list, delete_id)
            if deleted:
                save_tasks(current_list)
                print("Task has been removed")
            else:
                print("Task id not found")
        elif action == "mark":
            if len(command) < 3:
                print("Incorrect formatting")
                continue
            new_status = command[1].lower()
            if new_status not in VALID_STATUSES:
                print("Statuses are only to-do, in-progress, or done")
                continue
            try:
                mark_id = int(command[2])
            except ValueError:
                print("id must be an integer")
                continue
            marked = mark_task(current_list, new_status, mark_id)
            if marked:
                save_tasks(current_list)
                print(f"Task has been marked as {new_status}.")
            else:
                print("Task id not found")
        elif action == "list":
            if len(command) == 1:
                if not current_list:
                    print("No tasks found.")
                    continue
                for x in current_list:
                    print(f"{x['id']} {x['task']} {x['status']} Created: {x['createdAt']} Updated: {x['updatedAt']}")
            elif len(command) == 2:
                task_filter = command[1].lower()
                if task_filter not in VALID_STATUSES:
                    print("List filter not recognized")
                    continue
                for x in current_list:
                    if x['status'] == task_filter:
                        print(f"{x['id']} {x['task']} {x['status']} Created: {x['createdAt']} Updated: {x['updatedAt']}")
            else:
                print('List command not recognized')
        else:
            print("Command is unknown")
    
if __name__ == '__main__':
    main()
