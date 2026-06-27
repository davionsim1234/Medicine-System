"""
Question 3: Concurrent process
Factorial timing experiment using multithreading and non-multithreading.
"""

from dataclasses import dataclass
from threading import Thread
from time import perf_counter_ns


FACTORIAL_NUMBERS = [50, 100, 200]
ROUNDS = 10


@dataclass
class RoundResult:
    """Stores the timing result for one experiment round."""

    round_number: int
    total_time_ns: int


def factorial(number: int) -> int:
    """Calculate a factorial using an iterative loop with O(n) time complexity."""
    result = 1

    # The loop runs once for each integer from 2 up to number.
    for value in range(2, number + 1):
        result *= value

    return result


def calculate_factorial_for_thread(number: int, results: dict[int, int]) -> None:
    """Thread target function that calculates one factorial and stores the result."""
    results[number] = factorial(number)


def run_threaded_round(round_number: int) -> RoundResult:
    """Run one round where 50!, 100!, and 200! are calculated by separate threads."""
    results = {}
    threads = []

    # One separate thread is created for each factorial task, as required.
    for number in FACTORIAL_NUMBERS:
        thread = Thread(target=calculate_factorial_for_thread, args=(number, results))
        threads.append(thread)

    start_time = perf_counter_ns()

    # Starting all threads allows their work to overlap as concurrent execution.
    for thread in threads:
        thread.start()

    # Joining all threads ensures the total time ends after the last thread finishes.
    for thread in threads:
        thread.join()

    end_time = perf_counter_ns()
    total_time = end_time - start_time
    print(f"Threaded round {round_number}: T = {total_time} ns")
    return RoundResult(round_number, total_time)


def run_non_threaded_round(round_number: int) -> RoundResult:
    """Run one round where 50!, 100!, and 200! are calculated sequentially."""
    results = {}

    start_time = perf_counter_ns()

    # The same factorial tasks are completed one after another without threads.
    for number in FACTORIAL_NUMBERS:
        results[number] = factorial(number)

    end_time = perf_counter_ns()
    total_time = end_time - start_time
    print(f"Non-threaded round {round_number}: T = {total_time} ns")
    return RoundResult(round_number, total_time)


def calculate_total(results: list[RoundResult]) -> int:
    """Calculate the total time taken across all experiment rounds."""
    return sum(result.total_time_ns for result in results)


def calculate_average(results: list[RoundResult]) -> float:
    """Calculate the average nanosecond time for all experiment rounds."""
    return calculate_total(results) / len(results)


def display_factorial_values() -> None:
    """Display the factorial values used in the experiment."""
    print("\nFACTORIAL VALUES")
    for number in FACTORIAL_NUMBERS:
        print(f"{number}! = {factorial(number)}")


def run_threaded_experiment() -> list[RoundResult]:
    """Perform the required ten rounds using multithreading."""
    print("\nMULTITHREADED EXPERIMENT")
    threaded_results = []

    for round_number in range(1, ROUNDS + 1):
        threaded_results.append(run_threaded_round(round_number))

    # The total and average satisfy the required experiment measurements.
    total = calculate_total(threaded_results)
    average = calculate_average(threaded_results)
    print(f"Total threaded time   = {total} ns")
    print(f"Average threaded time = {average:.2f} ns")
    return threaded_results


def run_non_threaded_experiment() -> list[RoundResult]:
    """Perform the required ten rounds without multithreading."""
    print("\nNON-MULTITHREADED EXPERIMENT")
    non_threaded_results = []

    for round_number in range(1, ROUNDS + 1):
        non_threaded_results.append(run_non_threaded_round(round_number))

    # The total and average satisfy the required experiment measurements.
    total = calculate_total(non_threaded_results)
    average = calculate_average(non_threaded_results)
    print(f"Total non-threaded time   = {total} ns")
    print(f"Average non-threaded time = {average:.2f} ns")
    return non_threaded_results


def display_comparison(threaded_results: list[RoundResult], non_threaded_results: list[RoundResult]) -> None:
    """Display timing results side by side and explain the finding."""
    threaded_total = calculate_total(threaded_results)
    non_threaded_total = calculate_total(non_threaded_results)
    threaded_average = calculate_average(threaded_results)
    non_threaded_average = calculate_average(non_threaded_results)

    print("\nTHREADING COMPARISON")
    print("Round | Threaded T (ns) | Non-threaded T (ns)")
    print("-" * 48)

    for threaded, non_threaded in zip(threaded_results, non_threaded_results):
        print(
            f"{threaded.round_number:^5} | {threaded.total_time_ns:^15} | "
            f"{non_threaded.total_time_ns:^19}"
        )

    print("-" * 48)
    print(f"Total threaded time       : {threaded_total} ns")
    print(f"Total non-threaded time   : {non_threaded_total} ns")
    print(f"Average threaded time     : {threaded_average:.2f} ns")
    print(f"Average non-threaded time : {non_threaded_average:.2f} ns")
    print("\nAnalysis:")
    print(
        "In standard CPython, CPU-bound threads are concurrent but usually not truly "
        "parallel because the Global Interpreter Lock allows only one thread to "
        "execute Python bytecode at a time. Therefore, multithreading may not shorten "
        "this factorial experiment and can be slower because of thread-management overhead."
    )
    print(
        "Multithreading is more useful for input/output tasks such as downloading files, "
        "waiting for database responses, or reading many network requests."
    )


def explain_factorial_complexity() -> None:
    """Print the primitive-operation reasoning for the factorial function."""
    print("\nFACTORIAL TIME COMPLEXITY")
    print("For input n, the loop executes from 2 to n, so it performs n - 1 multiplications.")
    print("The number of operations grows linearly as n grows.")
    print("Therefore, the factorial function has O(n) time complexity.")


def run_experiment() -> None:
    """Run the full coursework experiment from start to finish."""
    display_factorial_values()
    explain_factorial_complexity()
    threaded_results = run_threaded_experiment()
    non_threaded_results = run_non_threaded_experiment()
    display_comparison(threaded_results, non_threaded_results)


if __name__ == "__main__":
    run_experiment()
