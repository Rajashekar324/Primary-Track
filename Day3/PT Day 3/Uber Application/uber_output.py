def show_locations(locations):
    print("\nAvailable Locations:")
    for i,loc in enumerate(locations,start=1):
        print(f"{i}. {loc}")
    print()
def show_trip(trip):
    print("\n--- Ride Details ---")
    print(f"Customer : {trip['customer_name']}")
    print(f"Phone    : {trip['masked_phone']}")
    print(f"Rider    : {trip['rider']}")
    print(f"Route    : {trip['route'][0]} -> {trip['route'][1]}")
    print(f"Distance : {trip['distance_km']} km")
    print(f"Fare     : ₹{trip['fare']}")
    print(f"Status   : {trip['status']}")
    print("Invoice generated: invoice.txt")
    print("--------------------\n")
    print("Thank you for riding with Mini Uber!\n")
    print("Have a great day!\n")
def show_cancelled():
    print("\nRide cancelled\n")
def show_all_rides(all_rides):
    if len(all_rides)==0:
        print("\nNo rides yet\n")
        return
    print("\n--- All Rides ---")
    for i, trip in enumerate(all_rides, start=1):
        r0, r1=trip["route"]
        print(f"{i}. {trip['rider']} | {r0} -> {r1} | {trip['distance_km']} km | ₹{trip['fare']} | {trip['status']}")
    print("---------------\n")
def show_profile(name, masked_phone, total_rides):
    print("\n--- Profile ---")
    print(f"Name       : {name}")
    print(f"Phone      : {masked_phone}")
    print(f"Total Rides: {total_rides}")
    print("------------\n")
