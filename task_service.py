from model import Task, ListOfTask, TaskListCollection, Status


class TaskService:
    def __init__(self, collection: TaskListCollection):
        self.collection = collection

    def add_list(self, list_of_tasks: ListOfTask):
        self.collection.task_groups.append(list_of_tasks)

    def add_task(self, task: Task, idx_list: int):
        return self.collection.task_groups[idx_list].list_task.append(task)

    def remove_task(self, idx_task: int, idx_list: int):
        del self.collection.task_groups[idx_list].list_task[idx_task]

    def remove_list(self, idx_list: int):
        del self.collection.task_groups[idx_list]

    def update_task_status(self, idx_list: int, idx_task: int, new_status: Status):
        self.collection.task_groups[idx_list].list_task[idx_task].status = new_status

    def update_list_status(self, idx_list: int, new_status: Status):
        self.collection.task_groups[idx_list].status = new_status
