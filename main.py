import model
from datetime import datetime
from task_service import TaskService

task = model.Task(
    id=1,
    title="Zrób śniadanie",
    description="Kango Kango Kango",
)
list = model.ListOfTask(id=1)
print(task)

TaskService.add_task(task, list)
print(list.list_task)
