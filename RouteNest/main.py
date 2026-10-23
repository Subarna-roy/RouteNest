"""
Intelligent Travel Route & Itinerary Planner
DAA Mini Project

Algorithms demonstrated:
1. Linear Search
2. Binary Search
3. Bubble Sort
4. Merge Sort
5. Quick Sort
6. Greedy Activity Selection
7. 0/1 Knapsack (Dynamic Programming)
8. BFS
9. DFS
10. Dijkstra's Shortest Path
11. Backtracking for itinerary generation
"""

import csv


# -------------------- DATA LOADING --------------------

def load_places(filename):
    places = []
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["cost"] = int(row["cost"])
            row["rating"] = float(row["rating"])
            row["time"] = int(row["time"])
            places.append(row)
    return places


def load_routes(filename):
    routes = []
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            routes.append((row["source"], row["destination"], int(row["distance"])))
    return routes


# -------------------- SEARCHING --------------------

def linear_search(places, name):
    # Time Complexity: O(n)
    for place in places:
        if place["name"].lower() == name.lower():
            return place
    return None


def binary_search(places, name):
    # Time Complexity: O(log n)
    sorted_places = sorted(places, key=lambda x: x["name"].lower())
    left, right = 0, len(sorted_places) - 1

    while left <= right:
        mid = (left + right) // 2
        current = sorted_places[mid]["name"].lower()

        if current == name.lower():
            return sorted_places[mid]
        elif current < name.lower():
            left = mid + 1
        else:
            right = mid - 1

    return None


# -------------------- SORTING --------------------

def bubble_sort(places):
    # Time Complexity: O(n^2)
    data = places[:]

    for i in range(len(data)):
        for j in range(0, len(data) - i - 1):
            if data[j]["rating"] < data[j + 1]["rating"]:
                data[j], data[j + 1] = data[j + 1], data[j]

    return data


def merge_sort(places):
    # Time Complexity: O(n log n)
    if len(places) <= 1:
        return places

    mid = len(places) // 2
    left = merge_sort(places[:mid])
    right = merge_sort(places[mid:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i]["rating"] >= right[j]["rating"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(places):
    # Average Time Complexity: O(n log n)
    if len(places) <= 1:
        return places

    pivot = places[-1]["rating"]
    smaller = [p for p in places[:-1] if p["rating"] >= pivot]
    greater = [p for p in places[:-1] if p["rating"] < pivot]

    return quick_sort(smaller) + [places[-1]] + quick_sort(greater)


# -------------------- GRAPH ALGORITHMS --------------------

def build_graph(routes):
    graph = {}

    for source, destination, distance in routes:
        graph.setdefault(source, []).append((destination, distance))
        graph.setdefault(destination, []).append((source, distance))

    return graph


def bfs(graph, start):
    # Time Complexity: O(V + E)
    visited = set()
    queue = [start]
    order = []

    while queue:
        current = queue.pop(0)

        if current in visited:
            continue

        visited.add(current)
        order.append(current)

        for neighbor, _ in graph.get(current, []):
            if neighbor not in visited:
                queue.append(neighbor)

    return order


def dfs(graph, start):
    # Time Complexity: O(V + E)
    visited = set()
    order = []

    def visit(node):
        visited.add(node)
        order.append(node)

        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                visit(neighbor)

    visit(start)
    return order


def dijkstra(graph, start, destination):
    # Time Complexity: O(V^2) with this simple implementation
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    unvisited = set(graph.keys())

    distances[start] = 0

    while unvisited:
        current = min(unvisited, key=lambda node: distances[node])

        if distances[current] == float("inf"):
            break

        unvisited.remove(current)

        if current == destination:
            break

        for neighbor, weight in graph.get(current, []):
            new_distance = distances[current] + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current

    if distances.get(destination, float("inf")) == float("inf"):
        return None, []

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()
    return distances[destination], path


# -------------------- GREEDY --------------------

def activity_selection(places, available_time):
    """
    Greedy activity selection:
    Choose attractions by earliest finishing time.
    For this project, 'time' is the visit duration.
    """
    selected = []
    total_time = 0

    # Greedy: shortest activities first to fit more activities.
    activities = sorted(places, key=lambda x: x["time"])

    for place in activities:
        if total_time + place["time"] <= available_time:
            selected.append(place)
            total_time += place["time"]

    return selected


# -------------------- DYNAMIC PROGRAMMING --------------------

def knapsack(places, budget):
    """
    0/1 Knapsack:
    Maximize total rating without exceeding the budget.
    Time Complexity: O(n * budget)
    """
    n = len(places)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = places[i - 1]["cost"]
        value = int(places[i - 1]["rating"] * 10)

        for b in range(budget + 1):
            if cost <= b:
                dp[i][b] = max(
                    dp[i - 1][b],
                    value + dp[i - 1][b - cost]
                )
            else:
                dp[i][b] = dp[i - 1][b]

    selected = []
    b = budget

    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            selected.append(places[i - 1])
            b -= places[i - 1]["cost"]

    selected.reverse()
    return selected, dp[n][budget] / 10


# -------------------- BACKTRACKING --------------------

def generate_itineraries(places, days, budget, max_results=5):
    """
    Generate valid small itineraries using backtracking.
    Constraint: total cost <= budget and number of places <= days.
    """

    results = []

    def backtrack(start, chosen, total_cost):
        if len(results) >= max_results:
            return

        if chosen:
            results.append((chosen[:], total_cost))

        if len(chosen) == days:
            return

        for i in range(start, len(places)):
            place = places[i]

            if total_cost + place["cost"] <= budget:
                chosen.append(place)
                backtrack(i + 1, chosen, total_cost + place["cost"])
                chosen.pop()

    backtrack(0, [], 0)
    return results


# -------------------- DISPLAY --------------------

def print_places(places):
    print("\n" + "-" * 72)
    print(f"{'Place':25} {'City':15} {'Cost':>8} {'Rating':>8} {'Time':>8}")
    print("-" * 72)

    for p in places:
        print(
            f"{p['name']:25} {p['city']:15} "
            f"₹{p['cost']:>6} {p['rating']:>7.1f} {p['time']:>6}h"
        )

    print("-" * 72)


def show_algorithm_menu():
    print("""
================ SMART TRAVEL PLANNER ================

1. Search a destination
2. Sort destinations by rating
3. Find shortest route
4. Explore cities using BFS
5. Explore cities using DFS
6. Best attractions within budget (0/1 Knapsack)
7. Select attractions using Greedy method
8. Generate possible itineraries (Backtracking)
9. Show DAA concepts and complexities
0. Exit
""")


def show_complexities():
    print("""
================ DAA ALGORITHM ANALYSIS ================

1. Linear Search
   Purpose: Find a destination.
   Complexity: O(n)

2. Binary Search
   Purpose: Find a destination in sorted data.
   Complexity: O(log n)

3. Bubble Sort
   Purpose: Sort destinations by rating.
   Complexity: O(n^2)

4. Merge Sort
   Purpose: Sort destinations by rating.
   Complexity: O(n log n)

5. Quick Sort
   Purpose: Sort destinations by rating.
   Average: O(n log n)
   Worst: O(n^2)

6. Greedy Activity Selection
   Purpose: Select attractions within available time.
   Complexity: O(n log n) because of sorting.

7. 0/1 Knapsack - Dynamic Programming
   Purpose: Select attractions within a budget.
   Complexity: O(n * budget)

8. BFS
   Purpose: Traverse connected travel locations.
   Complexity: O(V + E)

9. DFS
   Purpose: Traverse connected travel locations.
   Complexity: O(V + E)

10. Dijkstra
    Purpose: Find shortest travel route.
    Complexity: O(V^2) in this implementation.

11. Backtracking
    Purpose: Generate valid small itineraries.
    Worst case: Exponential.

==========================================================
""")


# -------------------- MAIN PROGRAM --------------------

def main():
    places = load_places("places.csv")
    routes = load_routes("routes.csv")
    graph = build_graph(routes)

    while True:
        show_algorithm_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter destination name: ").strip()

            result = linear_search(places, name)

            if result:
                print("\nLinear Search: Destination found!")
                print_places([result])

                binary_result = binary_search(places, name)
                if binary_result:
                    print("Binary Search: Destination also found.")
            else:
                print("\nDestination not found.")

        elif choice == "2":
            print("""
Choose sorting algorithm:
1. Bubble Sort
2. Merge Sort
3. Quick Sort
""")
            sort_choice = input("Enter choice: ").strip()

            if sort_choice == "1":
                result = bubble_sort(places)
                algorithm = "Bubble Sort"
            elif sort_choice == "2":
                result = merge_sort(places)
                algorithm = "Merge Sort"
            elif sort_choice == "3":
                result = quick_sort(places)
                algorithm = "Quick Sort"
            else:
                print("Invalid choice.")
                continue

            print(f"\nDestinations sorted using {algorithm}:")
            print_places(result)

        elif choice == "3":
            start = input("Enter source city: ").strip()
            destination = input("Enter destination city: ").strip()

            if start not in graph or destination not in graph:
                print("\nCity not found. Check the route dataset.")
                continue

            distance, path = dijkstra(graph, start, destination)

            if path:
                print("\nShortest route:")
                print(" -> ".join(path))
                print(f"Total distance: {distance} km")
            else:
                print("\nNo route found.")

        elif choice == "4":
            start = input("Enter starting city: ").strip()

            if start in graph:
                print("\nBFS Traversal:")
                print(" -> ".join(bfs(graph, start)))
            else:
                print("City not found.")

        elif choice == "5":
            start = input("Enter starting city: ").strip()

            if start in graph:
                print("\nDFS Traversal:")
                print(" -> ".join(dfs(graph, start)))
            else:
                print("City not found.")

        elif choice == "6":
            try:
                budget = int(input("Enter travel budget: ₹"))
                selected, value = knapsack(places, budget)

                print(f"\nBest attractions within ₹{budget}:")
                print_places(selected)
                print(f"Total rating value: {value:.1f}")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "7":
            try:
                hours = int(input("Enter available hours: "))

                selected = activity_selection(places, hours)

                print("\nGreedy selection:")
                print_places(selected)
                print(f"Total time used: {sum(p['time'] for p in selected)} hours")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "8":
            try:
                days = int(input("Maximum number of attractions: "))
                budget = int(input("Maximum budget: ₹"))

                results = generate_itineraries(places, days, budget)

                print("\nPossible itineraries:")
                for i, (itinerary, cost) in enumerate(results, 1):
                    names = " -> ".join(p["name"] for p in itinerary)
                    print(f"{i}. {names} | Cost: ₹{cost}")

                if not results:
                    print("No valid itinerary found.")
            except ValueError:
                print("Please enter valid numbers.")

        elif choice == "9":
            show_complexities()

        elif choice == "0":
            print("\nThank you for using Intelligent Travel Route & Itinerary Planner!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
