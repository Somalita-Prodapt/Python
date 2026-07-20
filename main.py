from data.seed_data import load_seed_data
from services.rental_system import RentalSystem


def print_menu():
    print("\n====== QUICKWHEELS VEHICLE RENTAL ======")
    print("1. Register customer")
    print("2. Add vehicle")
    print("3. View vehicles (sorted by rate)")
    print("4. Rent a vehicle")
    print("5. Return a vehicle")
    print("6. View rentals")
    print("7. Exit (archive rentals -> destructors fire)")


def main():
    load_seed_data()
    system = RentalSystem()

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
                pid = input("Customer ID: ").strip()
                name = input("Name: ").strip()
                age = int(input("Age: ").strip())
                phone = input("Phone: ").strip()
                license_no = input("License number (leave blank if none): ").strip() or None
                wallet_raw = input("Opening wallet balance [0]: ").strip()
                wallet = float(wallet_raw) if wallet_raw else 0
                cust = system.register_customer(pid, name, age, phone, license_no, wallet)
                print("Registered:", cust if cust else "Failed (duplicate ID?)")
            except ValueError:
                print("Invalid input, please enter numbers where expected.")

        elif choice == "2":
            try:
                vtype = input("Vehicle type (bike/car/suv): ").strip()
                rate = float(input("Daily rate: ").strip())
                name = input("Vehicle name: ").strip()
                vehicle = system.add_vehicle(vtype, rate, name)
                print("Added:", vehicle if vehicle else "Invalid vehicle type")
            except ValueError as e:
                print(f"Could not add vehicle: {e}")

        elif choice == "3":
            vehicles = system.view_vehicles_sorted()
            if not vehicles:
                print("No vehicles available.")
            for v in vehicles:
                print(v)

        elif choice == "4":
            cust_id = input("Customer ID: ").strip()
            veh_id = input("Vehicle ID: ").strip()
            try:
                days = int(input("Days: ").strip())
            except ValueError:
                print("Days must be a whole number.")
                continue
            rental, msg = system.rent_vehicle(cust_id, veh_id, days)
            print(msg)
            if rental:
                print(rental)

        elif choice == "5":
            try:
                rental_id = int(input("Rental ID: ").strip())
                actual_days = int(input("Actual days used: ").strip())
            except ValueError:
                print("Rental ID / actual days must be whole numbers.")
                continue
            damage_input = input("Damage note (leave blank if none): ").strip()
            damage_note = damage_input or None
            rental, msg = system.return_vehicle(rental_id, actual_days, damage_note)
            print(msg)

        elif choice == "6":
            rentals = system.view_rentals()
            if not rentals:
                print("No rentals yet.")
            for r in rentals:
                print(r)

        elif choice == "7":
            print("Archiving rentals...")
            system.archive_all_rentals()
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
