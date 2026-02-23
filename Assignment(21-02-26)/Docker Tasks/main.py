from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Simple in-memory "DB"
students = []
next_id = 1


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "students": students})


@app.get("/add", response_class=HTMLResponse)
async def add_page(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})


@app.post("/add")
async def add_student(name: str = Form(...), age: int = Form(...), course: str = Form(...)):
    global next_id
    students.append({"id": next_id, "name": name, "age": age, "course": course})
    next_id += 1
    return RedirectResponse(url="/", status_code=303)


@app.get("/view/{student_id}", response_class=HTMLResponse)
async def view_student(student_id: int, request: Request):
    st = next((s for s in students if s["id"] == student_id), None)
    if not st:
        raise HTTPException(status_code=404, detail="Student not found")
    return templates.TemplateResponse("view.html", {"request": request, "student": st})


@app.get("/edit/{student_id}", response_class=HTMLResponse)
async def edit_page(student_id: int, request: Request):
    st = next((s for s in students if s["id"] == student_id), None)
    if not st:
        raise HTTPException(status_code=404, detail="Student not found")
    return templates.TemplateResponse("edit.html", {"request": request, "student": st})


@app.post("/edit/{student_id}")
async def edit_student(
    student_id: int,
    name: str = Form(...),
    age: int = Form(...),
    course: str = Form(...)
):
    st = next((s for s in students if s["id"] == student_id), None)
    if not st:
        raise HTTPException(status_code=404, detail="Student not found")

    st["name"] = name
    st["age"] = age
    st["course"] = course
    return RedirectResponse(url=f"/view/{student_id}", status_code=303)


@app.post("/delete/{student_id}")
async def delete_student(student_id: int):
    global students
    students = [s for s in students if s["id"] != student_id]
    return RedirectResponse(url="/", status_code=303)