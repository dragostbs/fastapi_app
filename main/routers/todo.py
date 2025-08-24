from main.models.todo import Todo
from main.schemas.todo import TodoRequest
from main.database.utils import db_dependency, user_dependency
from fastapi import APIRouter, HTTPException, Path

router = APIRouter(
    prefix="/todo",
    tags=["todo"]
)

@router.get("/")
async def get_todo(db: db_dependency, user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")
        
        return db.query(Todo).filter(Todo.user_id == user.get("id")).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{todo_id}")
async def get_todo_by_id(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")
        
        todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == user.get("id")).first()

        if todo_model is None:
            raise HTTPException(status_code=404, detail="Todo not found...")
        
        return todo_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/")
async def add_todo(todo_request: TodoRequest, db: db_dependency, user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")

        todo_model = Todo(
            **todo_request.dict(), 
            user_id=user.get("id")
        )

        db.add(todo_model)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
@router.put("/{todo_id}")
async def change_todo(todo_request: TodoRequest, db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentification failed...")
        
        todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == user.get("id")).first()

        if todo_model is None:
            raise HTTPException(status_code=404, detail="Todo not found...")
        
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete

        db.add(todo_model)
        db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.delete("/{todo_id}")
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")
                
        todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == user.get("id")).first()

        if todo_model is None:
            raise HTTPException(status_code=404, detail="Todo not found...")
        
        db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == user.get("id")).delete()
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")