from datetime import datetime

from model import Task, ListOfTask, Status
from storage import Storage
from task_service import TaskService

DB_PATH = "tasks.json"


# ---------- helpers ----------


def next_id(items) -> int:
    """Returns the next free id (max + 1) for a list of objects with an .id field."""
    return max((item.id for item in items), default=0) + 1


def ask(prompt: str) -> str:
    return input(prompt).strip()


def ask_int(prompt: str):
    """Reads an integer; returns None on invalid input."""
    value = ask(prompt)
    try:
        return int(value)
    except ValueError:
        print("  ! Not a number.")
        return None


def pick_status():
    """Lets the user pick a status. Returns None if cancelled."""
    options = list(Status)
    print("  Pick a status:")
    for i, status in enumerate(options, start=1):
        print(f"   {i}. {status.value}")
    idx = ask_int("  > ")
    if idx is None or not (1 <= idx <= len(options)):
        print("  ! Invalid choice.")
        return None
    return options[idx - 1]


# ---------- display ----------


def show_all(service: TaskService):
    groups = service.collection.task_groups
    if not groups:
        print("\n(no lists yet - add one with option 2)\n")
        return
    print()
    for li, group in enumerate(groups):
        created = group.created_at.strftime("%Y-%m-%d %H:%M")
        print(
            f"[{li}] List #{group.id} | status: {group.status.value} | created: {created}"
        )
        if not group.list_task:
            print("    (no tasks)")
        for ti, task in enumerate(group.list_task):
            print(
                f"    ({ti}) #{task.id} [{task.status.value}] {task.title} - {task.description}"
            )
    print()


def pick_list_index(service: TaskService):
    """Asks for a list index and checks the range. Returns None on error."""
    groups = service.collection.task_groups
    if not groups:
        print("  ! Add a list first.")
        return None
    idx = ask_int("  List index [in square brackets]: ")
    if idx is None or not (0 <= idx < len(groups)):
        print("  ! No list with that index.")
        return None
    return idx


# ---------- actions ----------


def add_list(service: TaskService):
    group = ListOfTask(
        id=next_id(service.collection.task_groups),
        list_task=[],
        created_at=datetime.now(),
    )
    service.add_list(group)
    print(f"  + Added list #{group.id}.")


def add_task(service: TaskService):
    li = pick_list_index(service)
    if li is None:
        return
    title = ask("  Task title: ")
    if not title:
        print("  ! Title cannot be empty.")
        return
    description = ask("  Description: ")
    task = Task(
        id=next_id(service.collection.task_groups[li].list_task),
        title=title,
        description=description,
    )
    service.add_task(task, li)
    print(f"  + Added task #{task.id} to list [{li}].")


def remove_task(service: TaskService):
    li = pick_list_index(service)
    if li is None:
        return
    tasks = service.collection.task_groups[li].list_task
    if not tasks:
        print("  ! This list has no tasks.")
        return
    ti = ask_int("  Task index (in round brackets): ")
    if ti is None or not (0 <= ti < len(tasks)):
        print("  ! No task with that index.")
        return
    service.remove_task(ti, li)
    print("  - Removed task.")


def remove_list(service: TaskService):
    li = pick_list_index(service)
    if li is None:
        return
    service.remove_list(li)
    print("  - Removed list.")


def update_task_status(service: TaskService):
    li = pick_list_index(service)
    if li is None:
        return
    tasks = service.collection.task_groups[li].list_task
    if not tasks:
        print("  ! This list has no tasks.")
        return
    ti = ask_int("  Task index (in round brackets): ")
    if ti is None or not (0 <= ti < len(tasks)):
        print("  ! No task with that index.")
        return
    status = pick_status()
    if status is None:
        return
    service.update_task_status(li, ti, status)
    print("  * Task status updated.")


def update_list_status(service: TaskService):
    li = pick_list_index(service)
    if li is None:
        return
    status = pick_status()
    if status is None:
        return
    service.update_list_status(li, status)
    print("  * List status updated.")


# ---------- main loop ----------

MENU = """
==== Task Manager ====
1. Show all
2. Add list
3. Add task
4. Update task status
5. Update list status
6. Remove task
7. Remove list
8. Save
0. Save and exit
"""


def run():
    storage = Storage(DB_PATH)
    service = TaskService(storage.load())

    actions = {
        "1": lambda: show_all(service),
        "2": lambda: add_list(service),
        "3": lambda: add_task(service),
        "4": lambda: update_task_status(service),
        "5": lambda: update_list_status(service),
        "6": lambda: remove_task(service),
        "7": lambda: remove_list(service),
        "8": lambda: (storage.save(service.collection), print("  Saved.")),
    }

    while True:
        print(MENU)
        choice = ask("Choice: ")
        if choice == "0":
            storage.save(service.collection)
            print("Saved. Bye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("  ! Unknown option.")


if __name__ == "__main__":
    run()
