from uber_first import book_ride, get_all_rides, get_locations
from uber_output import show_trip, show_cancelled, show_all_rides, show_profile, show_locations
print("Welcome to Mini Uber\n")
name = input("Enter your name: ").strip()
phone = input("Enter your phone number: ").strip()
if len(phone)>=5:
    masked_phone=phone[:-5]+"*****"
else:
    masked_phone ="*****"
locations, location_set = get_locations()
def get_valid_location(msg):
    while True:
        loc=input(msg).strip()
        if loc in location_set:
            return loc
        print("Invalid location. Please enter from the available locations.")
while True:
    print("1. Book a ride")
    print("2. View all rides")
    print("3. Profile")
    print("4. Exit")
    choice=input("Enter choice: ").strip()
    if choice == "1":
        show_locations(locations)

        pickup = get_valid_location("Enter pickup location: ").title()
        while True:
            drop=get_valid_location("Enter drop location: ").title()
            if drop != pickup:
                break
            print("Pickup and drop cannot be the same. Enter a different drop location.")
        trip=book_ride(name,masked_phone, pickup, drop)
        if trip is None:
            show_cancelled()
        else:
            show_trip(trip)
    elif choice == "2":
        show_all_rides(get_all_rides())
    elif choice == "3":
        show_profile(name, masked_phone, len(get_all_rides()))
    elif choice == "4":
        print("\nThank you! Bye.\n")
        break
    else:
        print("\nInvalid choice\n")
