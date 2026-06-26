"""
Question 1: Hashing
Pharmacy inventory system using a hash table with linear probing.
"""

from dataclasses import dataclass
from sys import argv
from time import perf_counter_ns


@dataclass
class Medicine:
    """Entity class that represents one pharmacy product record."""

    medicine_id: str
    name: str
    category: str
    quantity: int
    price: float

    def display_row(self) -> str:
        """Format one medicine record so inventory output is easy to read."""
        return (
            f"{self.medicine_id:<8} | {self.name:<22} | {self.category:<12} | "
            f"{self.quantity:>8} | RM {self.price:>7.2f}"
        )


class HashTable:
    """Hash table that resolves collisions using linear probing."""

    DELETED = object()

    def __init__(self, size: int = 23):
        # The bucket structure is a fixed-size Python list.
        # Each bucket stores either None, a Medicine object, or the DELETED marker.
        self.size = size
        self.buckets = [None] * size
        self.count = 0

    def _hash(self, key: str) -> int:
        """Convert a medicine ID into a bucket index."""
        total = 0

        # Polynomial hashing spreads similar IDs, such as P0001 and P0002, across buckets.
        for character in key:
            total = (total * 31 + ord(character)) % self.size

        return total % self.size

    def _probe_indexes(self, key: str):
        """Generate every possible bucket index using linear probing."""
        start_index = self._hash(key)
        for step in range(self.size):
            yield (start_index + step) % self.size

    def insert(self, medicine: Medicine) -> bool:
        """Insert a new medicine or update an existing medicine with the same ID."""
        if self.count >= self.size:
            print("Hash table is full. New medicine cannot be inserted.")
            return False

        first_deleted_index = None

        # Linear probing checks the original hash position first, then the next buckets.
        for index in self._probe_indexes(medicine.medicine_id):
            bucket = self.buckets[index]

            if bucket is self.DELETED:
                if first_deleted_index is None:
                    first_deleted_index = index
                continue

            if bucket is None:
                target_index = first_deleted_index if first_deleted_index is not None else index
                self.buckets[target_index] = medicine
                self.count += 1
                return True

            if bucket.medicine_id == medicine.medicine_id:
                self.buckets[index] = medicine
                return True

        if first_deleted_index is not None:
            self.buckets[first_deleted_index] = medicine
            self.count += 1
            return True

        return False

    def search(self, medicine_id: str):
        """Search for a medicine by ID and return the Medicine object if found."""
        for index in self._probe_indexes(medicine_id):
            bucket = self.buckets[index]

            if bucket is None:
                return None

            if bucket is not self.DELETED and bucket.medicine_id == medicine_id:
                return bucket

        return None

    def delete(self, medicine_id: str) -> bool:
        """Delete a medicine record while keeping the probing chain searchable."""
        for index in self._probe_indexes(medicine_id):
            bucket = self.buckets[index]

            if bucket is None:
                return False

            if bucket is not self.DELETED and bucket.medicine_id == medicine_id:
                self.buckets[index] = self.DELETED
                self.count -= 1
                return True

        return False

    def display(self) -> None:
        """Display the current bucket index and record stored in each occupied bucket."""
        print("\nPHARMACY INVENTORY - HASH TABLE BUCKETS")
        print("Bucket | ID       | Name                   | Category     | Quantity | Price")
        print("-" * 84)

        for index, bucket in enumerate(self.buckets):
            if isinstance(bucket, Medicine):
                print(f"{index:^6} | {bucket.display_row()}")

        if self.count == 0:
            print("No medicine records are currently stored.")


def create_sample_medicines() -> list[Medicine]:
    """Create predefined sample records required by the coursework brief."""
    return [
        Medicine("M101", "Paracetamol 500mg", "Tablet", 120, 7.50),
        Medicine("M205", "Cough Syrup", "Syrup", 35, 12.90),
        Medicine("M309", "Vitamin C 1000mg", "Supplement", 80, 18.50),
        Medicine("M412", "Ibuprofen 200mg", "Tablet", 60, 9.90),
        Medicine("M518", "Antacid Chewable", "Tablet", 45, 11.20),
        Medicine("M623", "Saline Nasal Spray", "Spray", 25, 15.00),
        Medicine("M734", "Allergy Relief", "Tablet", 55, 13.40),
        Medicine("M845", "Electrolyte Sachet", "Supplement", 90, 16.80),
    ]


def linear_array_search(medicines: list[Medicine], medicine_id: str):
    """Search a one-dimensional array by checking each record one by one."""
    for medicine in medicines:
        if medicine.medicine_id == medicine_id:
            return medicine
    return None


def build_inventory() -> tuple[HashTable, list[Medicine]]:
    """Insert the same predefined records into a hash table and a normal list."""
    medicines = create_sample_medicines()
    hash_table = HashTable(size=23)

    for medicine in medicines:
        hash_table.insert(medicine)

    return hash_table, medicines


def create_performance_medicines(total_records: int = 1000) -> list[Medicine]:
    """Create a larger medicine dataset so the search experiment is meaningful."""
    categories = ["Tablet", "Syrup", "Supplement", "Spray"]
    medicines = []

    # A larger dataset shows the scaling difference between hashing and array search.
    for number in range(1, total_records + 1):
        medicines.append(
            Medicine(
                medicine_id=f"P{number:04d}",
                name=f"Sample Medicine {number}",
                category=categories[number % len(categories)],
                quantity=20 + (number % 150),
                price=5.0 + (number % 80) * 0.75,
            )
        )

    return medicines


def run_performance_comparison(hash_table: HashTable, medicines: list[Medicine]) -> None:
    """Compare hash-table searching with one-dimensional array searching."""
    performance_medicines = create_performance_medicines()
    performance_table = HashTable(size=2503)

    # The same records are inserted into both the hash table and one-dimensional array.
    for medicine in performance_medicines:
        performance_table.insert(medicine)

    search_keys = ["P0001", "P0250", "P0500", "P0750", "P1000", "P9999", "P0000"] * 1000

    start_hash = perf_counter_ns()
    for key in search_keys:
        performance_table.search(key)
    end_hash = perf_counter_ns()

    start_array = perf_counter_ns()
    for key in search_keys:
        linear_array_search(performance_medicines, key)
    end_array = perf_counter_ns()

    hash_time = end_hash - start_hash
    array_time = end_array - start_array

    print("\nSEARCH PERFORMANCE COMPARISON")
    print(f"Records in each structure      : {len(performance_medicines)}")
    print(f"Total searches performed       : {len(search_keys)}")
    print(f"Hash table search time         : {hash_time} ns")
    print(f"One-dimensional array time     : {array_time} ns")
    print(f"Average hash table search time : {hash_time / len(search_keys):.2f} ns")
    print(f"Average array search time      : {array_time / len(search_keys):.2f} ns")
    print("\nAnalysis:")
    print(
        "The hash table usually searches faster because the hash function calculates "
        "a likely bucket position directly. The array search must compare records "
        "from the beginning until it finds the ID or reaches the end."
    )


def prompt_new_medicine() -> Medicine:
    """Collect medicine details from the user for the insert feature."""
    medicine_id = input("Enter medicine ID: ").strip().upper()
    name = input("Enter medicine name: ").strip()
    category = input("Enter category: ").strip()
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: RM "))
    return Medicine(medicine_id, name, category, quantity, price)


def run_menu() -> None:
    """Command-line menu for the pharmacy inventory system."""
    hash_table, medicines = build_inventory()

    while True:
        print("\nPHARMACY INVENTORY MENU")
        print("1. Display all medicines")
        print("2. Insert medicine")
        print("3. Search medicine")
        print("4. Delete medicine")
        print("5. Run search performance comparison")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            hash_table.display()
        elif choice == "2":
            medicine = prompt_new_medicine()
            if hash_table.insert(medicine):
                medicines.append(medicine)
                print("Medicine inserted successfully.")
        elif choice == "3":
            medicine_id = input("Enter medicine ID to search: ").strip().upper()
            medicine = hash_table.search(medicine_id)
            print(medicine.display_row() if medicine else "Medicine not found.")
        elif choice == "4":
            medicine_id = input("Enter medicine ID to delete: ").strip().upper()
            print("Medicine deleted." if hash_table.delete(medicine_id) else "Medicine not found.")
        elif choice == "5":
            run_performance_comparison(hash_table, medicines)
        elif choice == "0":
            print("Program ended.")
            break
        else:
            print("Invalid option. Please try again.")


def run_demo() -> None:
    """Non-interactive demo used for testing and screenshots."""
    hash_table, medicines = build_inventory()
    hash_table.display()
    print("\nSearching for existing record M309:")
    print(hash_table.search("M309").display_row())
    print("\nSearching for non-existing record M999:")
    print(hash_table.search("M999"))
    run_performance_comparison(hash_table, medicines)


if __name__ == "__main__":
    if "--demo" in argv:
        run_demo()
    else:
        run_menu()
