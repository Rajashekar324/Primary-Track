
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

buses = {}
flights = {}
hotels = {}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/bus-ui", response_class=HTMLResponse)
def bus_page(request: Request):
    return templates.TemplateResponse("bus.html", {"request": request, "buses": buses})

@app.post("/create-bus")
def create_bus(bus_name: str = Form(...), total_seats: int = Form(...)):
    buses[bus_name] = {"total_seats": total_seats, "available_seats": total_seats, "booked_seats": []}
    return RedirectResponse("/bus-ui", status_code=303)

@app.post("/book-seat")
def book_seat(bus_name: str = Form(...), seat_number: int = Form(...)):
    bus = buses.get(bus_name)
    if bus and seat_number not in bus["booked_seats"]:
        bus["booked_seats"].append(seat_number)
        bus["available_seats"] -= 1
    return RedirectResponse("/bus-ui", status_code=303)

@app.get("/flight-ui", response_class=HTMLResponse)
def flight_page(request: Request):
    return templates.TemplateResponse("flight.html", {"request": request, "flights": flights})

@app.post("/create-flight")
def create_flight(flight_name: str = Form(...), total_seats: int = Form(...)):
    flights[flight_name] = {"total_seats": total_seats, "available_seats": total_seats}
    return RedirectResponse("/flight-ui", status_code=303)

@app.get("/hotel-ui", response_class=HTMLResponse)
def hotel_page(request: Request):
    return templates.TemplateResponse("hotel.html", {"request": request, "hotels": hotels})

@app.post("/create-hotel")
def create_hotel(hotel_name: str = Form(...), rooms: int = Form(...)):
    hotels[hotel_name] = {"total_rooms": rooms, "available_rooms": rooms}
    return RedirectResponse("/hotel-ui", status_code=303)
