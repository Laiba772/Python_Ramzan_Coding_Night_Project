import click     # to create a cli
import json      # to save and load tasks from a file
import os        # to check if the file exists

# Constants for file paths
TODO_FILE = "todo.json"

# funtion to load tasks.

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as file:
        return json.load(file)

# function to save tasks.

def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)    


@click.group()
def cli():
    """Simple Todo List Manager"""
    pass

@click.command()
@click.argument("task")
def add(task):
    """Add a new task to the list"""
    tasks = load_tasks()
    tasks.append({"task": task , "done": False})
    save_tasks(tasks)
    click.echo(f"Task added successfully: {task}")
 

@click.command()
def list():
    """List all the tasks"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks found")
        return
    for i, task in enumerate(tasks, 1):
        status = "✓" if task["done"] else "❌"
        click.echo(f"{i}. [{status}] {task['task']}")


@click.command()
@click.argument("task_id", type=int)
def complete(task_id):
    """Mark a task as done"""
    tasks = load_tasks()
    if 0 < task_id <= len(tasks):
        tasks[task_id - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"Task {task_id} marked as done")
    else:
        click.echo(f"Invalid task Id: {task_id}")   


@click.command()
@click.argument("task_id", type=int)
def remove(task_id):
    """Remove a task from the list"""
    tasks = load_tasks()
    if 0 < task_id <= len(tasks):
        removed_task = tasks.pop(task_id - 1)
        save_tasks(tasks)
        click.echo(f"Removed task: {removed_task['task']}")
    else:
        click.echo(f"Invalid task ID.")

cli.add_command(complete)
cli.add_command(list)
cli.add_command(add)
cli.add_command(remove)
if __name__ == "__main__":
    cli()    