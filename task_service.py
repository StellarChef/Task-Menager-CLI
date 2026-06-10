from model import Task, ListOfTask


class TaskService:
    def add_task(task: Task, list_of_tasks: ListOfTask):
        return list_of_tasks.list_task.append(task)

    def remove_task(task_index: int, list_of_tasks: ListOfTask):
        del list_of_tasks.list_task[task_index]
