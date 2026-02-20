from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import json

# =====================================================
# DATABASE SETUP
# =====================================================

DATABASE_URL = "sqlite:///./mmt.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

app = FastAPI(title="MakeMyTrip SQLAlchemy API")

# =====================================================
# DATABASE MODELS
# =====================================================

class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    total_seats = Column(Integer)
    available_seats = Column(Integer)
    booked_seats = Column(String)  # store as JSON string


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    total_seats = Column(Integer)
    available_seats = Column(Integer)


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    total_rooms = Column(Integer)
    available_rooms = Column(Integer)


Base.metadata.create_all(bind=engine)

# =====================================================
# Pydantic Schemas
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
# Dependency
# =====================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================================
# 🚌 BUS CRUD
# =====================================================

@app.post("/bus/{bus_name}")
def create_bus(bus_name: str, bus: BusCreate, db: Session = Depends(get_db)):
    existing = db.query(Bus).filter(Bus.name == bus_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bus already exists")

    new_bus = Bus(
        name=bus_name,
        total_seats=bus.total_seats,
        available_seats=bus.total_seats,
        booked_seats=json.dumps([])
    )

    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)

    return {"message": "Bus created successfully"}


@app.get("/bus")
def get_all_buses(db: Session = Depends(get_db)):
    buses = db.query(Bus).all()
    result = []
    for bus in buses:
        result.append({
            "name": bus.name,
            "total_seats": bus.total_seats,
            "available_seats": bus.available_seats,
            "booked_seats": json.loads(bus.booked_seats)
        })
    return result


@app.post("/bus/{bus_name}/seat")
def book_seat(bus_name: str, booking: SeatBooking, db: Session = Depends(get_db)):
    bus = db.query(Bus).filter(Bus.name == bus_name).first()

    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    seats = json.loads(bus.booked_seats)

    if booking.seat_number > bus.total_seats:
        raise HTTPException(status_code=400, detail="Invalid seat")

    if booking.seat_number in seats:
        raise HTTPException(status_code=400, detail="Seat already booked")

    seats.append(booking.seat_number)
    bus.available_seats -= 1
    bus.booked_seats = json.dumps(seats)

    db.commit()

    return {"message": "Seat booked successfully"}


@app.delete("/bus/{bus_name}")
def delete_bus(bus_name: str, db: Session = Depends(get_db)):
    bus = db.query(Bus).filter(Bus.name == bus_name).first()

    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    db.delete(bus)
    db.commit()

    return {"message": "Bus deleted"}

# =====================================================
# ✈ FLIGHT CRUD
# =====================================================

@app.post("/flight/{flight_name}")
def create_flight(flight_name: str, flight: FlightCreate, db: Session = Depends(get_db)):
    new_flight = Flight(
        name=flight_name,
        total_seats=flight.total_seats,
        available_seats=flight.total_seats
    )
    db.add(new_flight)
    db.commit()
    return {"message": "Flight created"}


@app.get("/flight")
def get_flights(db: Session = Depends(get_db)):
    return db.query(Flight).all()


@app.delete("/flight/{flight_name}")
def delete_flight(flight_name: str, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.name == flight_name).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    db.delete(flight)
    db.commit()
    return {"message": "Flight deleted"}

# =====================================================
# 🏨 HOTEL CRUD
# =====================================================

@app.post("/hotel/{hotel_name}")
def create_hotel(hotel_name: str, hotel: HotelCreate, db: Session = Depends(get_db)):
    new_hotel = Hotel(
        name=hotel_name,
        total_rooms=hotel.total_rooms,
        available_rooms=hotel.total_rooms
    )
    db.add(new_hotel)
    db.commit()
    return {"message": "Hotel created"}


@app.get("/hotel")
def get_hotels(db: Session = Depends(get_db)):
    return db.query(Hotel).all()


@app.delete("/hotel/{hotel_name}")
def delete_hotel(hotel_name: str, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.name == hotel_name).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    db.delete(hotel)
    db.commit()
    return {"message": "Hotel deleted"}