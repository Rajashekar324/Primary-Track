from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="MakeMyTrip Clone API")

# =====================================================
# In-memory database
# =====================================================

buses: Dict[str, dict] = {}
flights: Dict[str, dict] = {}
hotels: Dict[str, dict] = {}

# =====================================================
# Pydantic Models
# =====================================================

class BusCreate(BaseModel):
    total_seats: int

class SeatBooking(BaseModel):
    seat_number: int

class SeatUpdate(BaseModel):
    old_seat: int
    new_seat: int

class FlightCreate(BaseModel):
    total_seats: int

class HotelCreate(BaseModel):
    total_rooms: int


# =====================================================
# 🚌 BUS CRUD + BOOKING
# =====================================================

# Get all buses
@app.get("/bus")
def get_all_buses():
    return buses


# Get individual bus
@app.get("/bus/{bus_name}")
def get_bus(bus_name: str):
    if bus_name not in buses:
        raise HTTPException(status_code=404, detail="Bus not found")
    return buses[bus_name]


# Search bus
@app.get("/bus/search/")
def search_bus(busname: str):
    result = {k: v for k, v in buses.items() if busname.lower() in k.lower()}
    return result


# Create bus
@app.post("/bus/{bus_name}")
def create_bus(bus_name: str, bus: BusCreate):
    if bus_name in buses:
        raise HTTPException(status_code=400, detail="Bus already exists")

    buses[bus_name] = {
        "total_seats": bus.total_seats,
        "available_seats": bus.total_seats,
        "booked_seats": []
    }

    return {"message": "Bus created successfully", "data": buses[bus_name]}


# Book seat
@app.post("/bus/{bus_name}/seat")
def book_seat(bus_name: str, booking: SeatBooking):
    if bus_name not in buses:
        raise HTTPException(status_code=404, detail="Bus not found")

    bus = buses[bus_name]

    if booking.seat_number > bus["total_seats"]:
        raise HTTPException(status_code=400, detail="Invalid seat number")

    if booking.seat_number in bus["booked_seats"]:
        raise HTTPException(status_code=400, detail="Seat already booked")

    bus["booked_seats"].append(booking.seat_number)
    bus["available_seats"] -= 1

    return {"message": "Seat booked successfully"}


# Update seat
@app.put("/bus/{bus_name}/seat")
def update_seat(bus_name: str, update: SeatUpdate):
    if bus_name not in buses:
        raise HTTPException(status_code=404, detail="Bus not found")

    bus = buses[bus_name]

    if update.old_seat not in bus["booked_seats"]:
        raise HTTPException(status_code=404, detail="Old seat not booked")

    if update.new_seat in bus["booked_seats"]:
        raise HTTPException(status_code=400, detail="New seat already booked")

    bus["booked_seats"].remove(update.old_seat)
    bus["booked_seats"].append(update.new_seat)

    return {"message": "Seat updated successfully"}


# Confirm booking
@app.get("/bus/{bus_name}/seat")
def confirm_booking(bus_name: str):
    if bus_name not in buses:
        raise HTTPException(status_code=404, detail="Bus not found")

    return {
        "bus": bus_name,
        "booked_seats": buses[bus_name]["booked_seats"]
    }


# Delete bus
@app.delete("/bus/{bus_name}")
def delete_bus(bus_name: str):
    if bus_name not in buses:
        raise HTTPException(status_code=404, detail="Bus not found")

    del buses[bus_name]
    return {"message": "Bus deleted successfully"}


# =====================================================
# ✈ FLIGHT CRUD
# =====================================================

@app.get("/flight")
def get_all_flights():
    return flights


@app.get("/flight/{flight_name}")
def get_flight(flight_name: str):
    if flight_name not in flights:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flights[flight_name]


@app.post("/flight/{flight_name}")
def create_flight(flight_name: str, flight: FlightCreate):
    if flight_name in flights:
        raise HTTPException(status_code=400, detail="Flight already exists")

    flights[flight_name] = {
        "total_seats": flight.total_seats,
        "available_seats": flight.total_seats
    }

    return {"message": "Flight created successfully", "data": flights[flight_name]}


@app.put("/flight/{flight_name}")
def update_flight(flight_name: str, flight: FlightCreate):
    if flight_name not in flights:
        raise HTTPException(status_code=404, detail="Flight not found")

    flights[flight_name]["total_seats"] = flight.total_seats
    flights[flight_name]["available_seats"] = flight.total_seats

    return {"message": "Flight updated successfully"}


@app.delete("/flight/{flight_name}")
def delete_flight(flight_name: str):
    if flight_name not in flights:
        raise HTTPException(status_code=404, detail="Flight not found")

    del flights[flight_name]
    return {"message": "Flight deleted successfully"}


# =====================================================
# 🏨 HOTEL CRUD
# =====================================================

@app.get("/hotel")
def get_all_hotels():
    return hotels


@app.get("/hotel/{hotel_name}")
def get_hotel(hotel_name: str):
    if hotel_name not in hotels:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotels[hotel_name]


@app.post("/hotel/{hotel_name}")
def create_hotel(hotel_name: str, hotel: HotelCreate):
    if hotel_name in hotels:
        raise HTTPException(status_code=400, detail="Hotel already exists")

    hotels[hotel_name] = {
        "total_rooms": hotel.total_rooms,
        "available_rooms": hotel.total_rooms
    }

    return {"message": "Hotel created successfully", "data": hotels[hotel_name]}


@app.put("/hotel/{hotel_name}")
def update_hotel(hotel_name: str, hotel: HotelCreate):
    if hotel_name not in hotels:
        raise HTTPException(status_code=404, detail="Hotel not found")

    hotels[hotel_name]["total_rooms"] = hotel.total_rooms
    hotels[hotel_name]["available_rooms"] = hotel.total_rooms

    return {"message": "Hotel updated successfully"}


@app.delete("/hotel/{hotel_name}")
def delete_hotel(hotel_name: str):
    if hotel_name not in hotels:
        raise HTTPException(status_code=404, detail="Hotel not found")

    del hotels[hotel_name]
    return {"message": "Hotel deleted successfully"}