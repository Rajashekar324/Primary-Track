import time
riders=[
    {"id":1,"name":"Arjun"},
    {"id":2,"name":"Meera"},
    {"id":3,"name":"Sanjay"}
]
available={1,2,3}
def book_ride(pickup,drop):
    pickup=pickup.strip()
    drop=drop.strip()
    route=(pickup,drop)
    if len(available)==0:
        return None
    rider_id=available.pop()
    rider_name=""
    for r in riders:
        if r["id"]==rider_id:
            rider_name=r["name"]
            break
    trip={
        "pickup": route[0],
        "drop": route[1],
        "rider": rider_name,
        "status": "Booked"
    }
    trip["status"]="Rider on the way"
    time.sleep(2)
    trip["status"]="Picked up"
    time.sleep(5)
    trip["status"]="Dropped"
    time.sleep(2)
    trip["status"]="Ride Completed"
    available.add(rider_id)
    return trip
