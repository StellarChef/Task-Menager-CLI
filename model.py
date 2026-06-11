from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class Status(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    Done = "done"


class Task(BaseModel):
    id: int
    title: str
    status: Status = (
        Status.NEW
    )  # To refer dircetly to Enum class status y've to do this.
    description: str


class ListOfTask(BaseModel):
    id: int
    list_task: list[Task]
    status: Status = Status.NEW
    created_at: datetime


class TaskListCollection(BaseModel):
    task_groups: list[ListOfTask]
