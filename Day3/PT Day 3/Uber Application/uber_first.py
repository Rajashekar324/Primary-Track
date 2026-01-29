import os
import time
rides=[]
locations = ["Madhapur","Gachibowli","Hitech City","Ameerpet","Kukatpally"]
location_set=set(locations)
distance_table={
    ("Ameerpet","Gachibowli"):12,
    ("Ameerpet","Hitech City"):8,
    ("Ameerpet","Kukatpally"):10,
    ("Ameerpet","Madhapur"):7,
    ("Gachibowli","Hitech City"):6,
    ("Gachibowli","Kukatpally"):15,
    ("Gachibowli","Madhapur"):9,
    ("Hitech City","Kukatpally"):13,
    ("Hitech City","Madhapur"):4,
    ("Kukatpally","Madhapur"):11
}
def get_distance(pickup,drop):
    a,b=sorted([pickup,drop])
    return distance_table[(a,b)]
def calculate_fare(distance_km):
    base=50
    per_km=15
    return base+(per_km*distance_km)
def calculate_fare(distance_km):
    base=50
    per_km=15
    return base+(per_km * distance_km)
def create_invoice(trip):
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "invoice.txt")
    f = open(path, "w", encoding="utf-8")
    f.write("========== MINI UBER INVOICE ==========\n")
    f.write(f"Customer : {trip['customer_name']}\n")
    f.write(f"Phone    : {trip['masked_phone']}\n")
    f.write("--------------------------------------\n")
    f.write(f"Rider    : {trip['rider']}\n")
    f.write(f"Route    : {trip['route'][0]} -> {trip['route'][1]}\n")
    f.write(f"Distance : {trip['distance_km']} km\n")
    f.write(f"Fare     : ₹{trip['fare']}\n")
    f.write(f"Status   : {trip['status']}\n")
    f.write("======================================\n")
    f.close()
def book_ride(customer_name,masked_phone,pickup,drop):
    pickup=pickup.strip()
    drop=drop.strip()
    rider_list=["Arjun", "Meera", "Sanjay"]
    rider=rider_list[len(rides) % len(rider_list)]
    route=(pickup, drop)
    distance_km=get_distance(pickup,drop)
    fare=calculate_fare(distance_km)
    trip={
        "customer_name":customer_name,
        "masked_phone":masked_phone,
        "rider":rider,
        "route":route,
        "distance_km":distance_km,
        "fare":fare,
        "status":"Booked"
    }
    accept=input(f"Rider {rider} allocated. Accept rider? (yes/no): ").strip().lower()
    if accept!="yes":
        return None
    print("Rider accepted successfully!")
    print("Waiting for the rider...")
    time.sleep(2)
    start=input("Start ride? (Yes/No): ").strip().lower()
    if start!="yes":
        return None
    trip["status"]="Ride Started"
    time.sleep(2)
    complete=input("Complete ride? (yes/no): ").strip().lower()
    if complete!="yes":
        return None
    trip["status"]="Ride Completed"
    print("\nBill status:")
    print("1. Paid")
    print("2. Pending")
    pay_choice=input("Enter choice: ").strip()
    if pay_choice=="1":
        trip["payment_status"]="Paid"
        print("Thank you for your payment!")
    else:
        trip["payment_status"] = "Pending"
        print("Please pay the pending amount at the end of the ride.")
    create_invoice(trip)
    rides.append(trip)
    return trip
def get_all_rides():
    return rides
def get_locations():
    return locations, location_set

