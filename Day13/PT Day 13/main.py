from contextlib import asynccontextmanager
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


# ---------- Models ----------
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    # Allow client to optionally send an ID so we can test duplicate IDs.
    id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None
    completed: Optional[bool] = None


class Task(TaskBase):
    id: int


# ---------- In-memory store initialization ----------
def _init_state(app: FastAPI):
    if not hasattr(app.state, "tasks"):
        app.state.tasks = {}  # type: ignore[attr-defined]
    if not hasattr(app.state, "next_id"):
        app.state.next_id = 1  # type: ignore[attr-defined]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    _init_state(app)
    yield
    # Shutdown


def create_app() -> FastAPI:
    """Factory function to create and configure the FastAPI app."""
    app = FastAPI(title="Tasks API", lifespan=lifespan)

    # ---------- Validation -> 400 (instead of FastAPI default 422) ----------
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.errors()},
        )

    def _get_task_or_404(task_id: int) -> Task:
        tasks: Dict[int, Task] = app.state.tasks  # type: ignore[attr-defined]
        if task_id not in tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        return tasks[task_id]

    # ---------- Routes ----------
    @app.get("/api/tasks", response_model=List[Task])
    def get_all_tasks():
        tasks: Dict[int, Task] = app.state.tasks  # type: ignore[attr-defined]
        return list(tasks.values())

    @app.get("/api/tasks/{task_id}", response_model=Task)
    def get_single_task(task_id: int):
        return _get_task_or_404(task_id)

    @app.post("/api/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
    def create_task(payload: TaskCreate):
        tasks: Dict[int, Task] = app.state.tasks  # type: ignore[attr-defined]

        # If client provides ID, enforce uniqueness (for "Duplicate IDs" case)
        if payload.id is not None:
            if payload.id in tasks:
                raise HTTPException(status_code=409, detail="Task ID already exists")
            new_id = payload.id
        else:
            new_id = app.state.next_id  # type: ignore[attr-defined]
            app.state.next_id += 1  # type: ignore[attr-defined]

        task = Task(id=new_id, title=payload.title, description=payload.description, completed=payload.completed)
        tasks[new_id] = task
        return task

    @app.put("/api/tasks/{task_id}", response_model=Task)
    def update_task(task_id: int, payload: TaskUpdate):
        tasks: Dict[int, Task] = app.state.tasks  # type: ignore[attr-defined]

        if task_id not in tasks:
            raise HTTPException(status_code=404, detail="Task not found")

        existing = tasks[task_id]
        updated = existing.model_copy(
            update={k: v for k, v in payload.model_dump().items() if v is not None}
        )
        tasks[task_id] = updated
        return updated

    @app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_task(task_id: int):
        tasks: Dict[int, Task] = app.state.tasks  # type: ignore[attr-defined]

        if task_id not in tasks:
            raise HTTPException(status_code=404, detail="Task not found")

        del tasks[task_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return app


app = create_app()
