from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Annotated
from database import cursor, get_tasks, add_task, update_task as db_update_task, delete_task as db_delete_task


router = APIRouter(
    prefix="/tasks",
    tags=["Your tasks"],
)

class TaskCreate(BaseModel):
    title: str
    priority: int = Field(
        ge=1,
        le=5,
        description="Priority from 1 to 5."
    )
    is_completed: bool = False
    

class TaskResponse(BaseModel):
    id: int
    title: str
    priority: int
    is_completed: bool


@router.get("")
def get_all_tasks(
    search: Annotated[
        str | None, 
        Query(description="Search by title")
    ] = None
):
    
    filtered_tasks = []
    
    if search is None:
        return get_tasks()
    
    else:
        for task in get_tasks():
            if search.lower() in task[1].lower():
                filtered_tasks.append(task)
                
    return filtered_tasks


@router.get("/{task_id}")
def read_task(task_id: int):
    
    for item in get_tasks():
        if item[0] == task_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="This task does not exist!"
    )


@router.post("", status_code=201)
def create_task(task: TaskCreate):
    task_dict = task.model_dump()
    add_task(task.title, task.priority, task.is_completed)
    id_task = cursor.lastrowid
    
    return {
        "message": "Task created!",
        "task": {
            "id": id_task,
            "title": task.title,
            "priority": task.priority,
            "is_completed": task.is_completed
        }
    }


@router.put("/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    
    for item in get_tasks():
        if item[0] == task_id:
            db_update_task(task.title, task.priority, task.is_completed, task_id)

            return {
                "message": "Task updated!",
                "task": {
                    "id": task_id,
                    "title": task.title,
                    "priority": task.priority,
                    "is_completed": task.is_completed
                }
            }
    
    raise HTTPException(status_code=404)

@router.delete("/{task_id}")
def delete_task(task_id: int):
    
    for item in get_tasks():
        if item[0] == task_id:
            db_delete_task(task_id)
            return {"message": "Task removed!",
                    "task": item
            }
            
    raise HTTPException(
        status_code=404,
        detail="This task does not exist! "
    )