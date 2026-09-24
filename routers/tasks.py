from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import Task
from auth import get_current_user
from schemas import TaskCreate,TaskResponse,TaskUpdate


router = APIRouter() #router = пачка маршрутів, яку ми потім підключаємо до app.


@router.post('/tasks', response_model=TaskResponse,status_code = 201)
def create_task(task:TaskCreate,db=Depends(get_db),current_user = Depends(get_current_user)):
    new_task = Task(title = task.title,completed = task.completed,user_id = current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get('/tasks', response_model=list[TaskResponse])
def get_user_tasks(current_user = Depends(get_current_user),db=Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()


    return tasks

@router.patch('/tasks/{task_id}', response_model=TaskResponse)
def update_task(task_id:int,task:TaskUpdate,db=Depends(get_db),current_user = Depends(get_current_user)):
    find_task = db.query(Task).filter(Task.id == task_id,Task.user_id == current_user.id).first()
    if find_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.title is not None:
        find_task.title = task.title
    if task.completed is not None:
        find_task.completed = task.completed

    db.commit()
    db.refresh(find_task)

    return find_task


@router.delete('/tasks/{task_id}')
def delete_task(task_id:int,db=Depends(get_db),current_user = Depends(get_current_user)):
    find_task = db.query(Task).filter(Task.id == task_id,Task.user_id == current_user.id).first()
    if find_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(find_task)
    db.commit()

    return {'Message': 'Task deleted successfully'}
