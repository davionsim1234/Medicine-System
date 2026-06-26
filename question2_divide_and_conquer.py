"""
Question 2: Divide and Conquer Algorithm
Transaction sorting and searching system using Merge Sort and Binary Search.
"""

from dataclasses import dataclass
from sys import argv
from time import perf_counter_ns


@dataclass
class Transaction:
    """Entity class that represents one online shopping transaction."""

    transaction_id: int
    customer_name: str
    product_name: str
    amount: float
    transaction_date: str

    def display_row(self) -> str:
        """Format one transaction record for clear command-line output."""
        return (
            f"{self.transaction_id:<6} | {self.customer_name:<14} | "
            f"{self.product_name:<18} | RM {self.amount:>8.2f} | {self.transaction_date}"
        )


def create_unsorted_transactions() -> list[Transaction]:
    """Create an initially unsorted dataset between 10 and 30 records."""
    return [
        Transaction(1087, "Aina", "Keyboard", 159.90, "2026-04-02"),
        Transaction(1021, "Brandon", "USB-C Cable", 29.90, "2026-04-04"),
        Transaction(1114, "Chloe", "Laptop Stand", 89.50, "2026-04-01"),
        Transaction(1005, "Daniel", "Wireless Mouse", 74.90, "2026-04-05"),
        Transaction(1068, "Elena", "Monitor", 699.00, "2026-04-08"),
        Transaction(1132, "Farah", "Webcam", 139.00, "2026-04-03"),
        Transaction(1044, "Gavin", "Headset", 219.90, "2026-04-07"),
        Transaction(1099, "Hana", "Power Bank", 119.00, "2026-04-06"),
        Transaction(1012, "Isaac", "Tablet Case", 49.90, "2026-04-10"),
        Transaction(1150, "Jia", "External SSD", 399.00, "2026-04-09"),
        Transaction(1033, "Kumar", "HDMI Adapter", 35.00, "2026-04-11"),
        Transaction(1108, "Lina", "Smart Speaker", 249.00, "2026-04-12"),
    ]


def display_transactions(transactions: list[Transaction], title: str = "TRANSACTIONS") -> None:
    """Display all transactions in a readable table."""
    print(f"\n{title}")
    print("ID     | Customer       | Product            | Amount      | Date")
    print("-" * 76)

    for transaction in transactions:
        print(transaction.display_row())

    if not transactions:
        print("No transaction records are available.")


def merge(left: list[Transaction], right: list[Transaction], key_name: str) -> list[Transaction]:
    """Combine two sorted lists into one sorted list."""
    combined = []
    left_index = 0
    right_index = 0

    # The combine step repeatedly selects the smaller current item.
    while left_index < len(left) and right_index < len(right):
        if getattr(left[left_index], key_name) <= getattr(right[right_index], key_name):
            combined.append(left[left_index])
            left_index += 1
        else:
            combined.append(right[right_index])
            right_index += 1

    combined.extend(left[left_index:])
    combined.extend(right[right_index:])
    return combined


def merge_sort(
    transactions: list[Transaction],
    key_name: str = "transaction_id",
    depth: int = 0,
    show_calls: bool = False,
    call_counter: dict[str, int] | None = None,
) -> list[Transaction]:
    """Sort transactions recursively using divide, conquer, and combine steps."""
    if call_counter is not None:
        call_counter["calls"] += 1

    if show_calls:
        print("  " * depth + f"merge_sort called with {len(transactions)} record(s)")

    # Base case: a list with zero or one record is already sorted.
    if len(transactions) <= 1:
        return transactions[:]

    # Divide step: split the dataset into left and right halves.
    middle = len(transactions) // 2
    left_half = transactions[:middle]
    right_half = transactions[middle:]

    # Conquer step: recursively sort both halves.
    sorted_left = merge_sort(left_half, key_name, depth + 1, show_calls, call_counter)
    sorted_right = merge_sort(right_half, key_name, depth + 1, show_calls, call_counter)

    # Combine step: merge both sorted halves into one sorted list.
    return merge(sorted_left, sorted_right, key_name)


def binary_search(transactions: list[Transaction], target_id: int):
    """Search a sorted transaction list using binary search."""
    low = 0
    high = len(transactions) - 1

    while low <= high:
        middle = (low + high) // 2
        middle_id = transactions[middle].transaction_id

        if middle_id == target_id:
            return transactions[middle]
        if target_id < middle_id:
            high = middle - 1
        else:
            low = middle + 1

    return None


def linear_search(transactions: list[Transaction], target_id: int):
    """Search an unsorted or sorted transaction list one record at a time."""
    for transaction in transactions:
        if transaction.transaction_id == target_id:
            return transaction
    return None


def compare_performance(transactions: list[Transaction]) -> None:
    """Measure Merge Sort, Binary Search, and Linear Search execution time."""
    existing_id = 1108
    missing_id = 9999

    start_sort = perf_counter_ns()
    sorted_transactions = merge_sort(transactions)
    end_sort = perf_counter_ns()

    start_binary = perf_counter_ns()
    binary_search(sorted_transactions, existing_id)
    binary_search(sorted_transactions, missing_id)
    end_binary = perf_counter_ns()

    start_linear = perf_counter_ns()
    linear_search(transactions, existing_id)
    linear_search(transactions, missing_id)
    end_linear = perf_counter_ns()

    print("\nPERFORMANCE COMPARISON")
    print(f"Merge Sort time                         : {end_sort - start_sort} ns")
    print(f"Binary Search time for 2 searches        : {end_binary - start_binary} ns")
    print(f"Linear Search time for 2 searches        : {end_linear - start_linear} ns")
    print("\nAnalysis:")
    print(
        "Merge Sort takes more time than one search because it processes the whole list "
        "to arrange the data. After sorting, Binary Search is efficient because it "
        "cuts the search range in half during each step."
    )


def prompt_transaction() -> Transaction:
    """Collect transaction details for the optional insert feature."""
    transaction_id = int(input("Enter transaction ID: "))
    customer_name = input("Enter customer name: ").strip()
    product_name = input("Enter product name: ").strip()
    amount = float(input("Enter amount: RM "))
    transaction_date = input("Enter date (YYYY-MM-DD): ").strip()
    return Transaction(transaction_id, customer_name, product_name, amount, transaction_date)


def show_complexity_table() -> None:
    """Display time complexity analysis as an optional advanced feature."""
    print("\nTIME COMPLEXITY ANALYSIS")
    print("Operation       | Best Case  | Average Case | Worst Case")
    print("-" * 58)
    print("Merge Sort      | O(n log n) | O(n log n)   | O(n log n)")
    print("Binary Search   | O(1)       | O(log n)     | O(log n)")
    print("Linear Search   | O(1)       | O(n)         | O(n)")


def run_menu() -> None:
    """Menu-driven program containing all mandatory and selected advanced features."""
    transactions = create_unsorted_transactions()
    sorted_transactions = []

    while True:
        print("\nTRANSACTION SYSTEM MENU")
        print("1. Display all transactions")
        print("2. Sort transactions by transaction ID using Merge Sort")
        print("3. Search transaction using Binary Search")
        print("4. Search transaction using Linear Search")
        print("5. Insert new transaction")
        print("6. Sort transactions by amount")
        print("7. Show complexity table")
        print("8. Compare performance")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_transactions(transactions, "CURRENT TRANSACTIONS")
        elif choice == "2":
            print("\nRecursive calls during Merge Sort:")
            counter = {"calls": 0}
            display_transactions(transactions, "BEFORE SORTING")
            sorted_transactions = merge_sort(transactions, show_calls=True, call_counter=counter)
            transactions = sorted_transactions
            display_transactions(transactions, "AFTER SORTING BY TRANSACTION ID")
            print(f"Total recursive calls: {counter['calls']}")
        elif choice == "3":
            if not sorted_transactions:
                sorted_transactions = merge_sort(transactions)
            target_id = int(input("Enter transaction ID to search: "))
            result = binary_search(sorted_transactions, target_id)
            print(result.display_row() if result else "Transaction not found.")
        elif choice == "4":
            target_id = int(input("Enter transaction ID to search: "))
            result = linear_search(transactions, target_id)
            print(result.display_row() if result else "Transaction not found.")
        elif choice == "5":
            transactions.append(prompt_transaction())
            sorted_transactions = []
            print("Transaction inserted successfully.")
        elif choice == "6":
            transactions = merge_sort(transactions, key_name="amount")
            sorted_transactions = []
            display_transactions(transactions, "AFTER SORTING BY AMOUNT")
        elif choice == "7":
            show_complexity_table()
        elif choice == "8":
            compare_performance(transactions)
        elif choice == "0":
            print("Program ended.")
            break
        else:
            print("Invalid option. Please try again.")


def run_demo() -> None:
    """Non-interactive demo used for testing and screenshots."""
    transactions = create_unsorted_transactions()
    display_transactions(transactions, "BEFORE SORTING")
    counter = {"calls": 0}
    sorted_transactions = merge_sort(transactions, show_calls=True, call_counter=counter)
    display_transactions(sorted_transactions, "AFTER SORTING BY TRANSACTION ID")
    print(f"Total recursive calls: {counter['calls']}")
    print("\nBinary Search for existing ID 1108:")
    print(binary_search(sorted_transactions, 1108).display_row())
    print("\nBinary Search for non-existing ID 9999:")
    print(binary_search(sorted_transactions, 9999))
    print("\nLinear Search for existing ID 1044:")
    print(linear_search(transactions, 1044).display_row())
    show_complexity_table()
    compare_performance(transactions)


if __name__ == "__main__":
    if "--demo" in argv:
        run_demo()
    else:
        run_menu()
