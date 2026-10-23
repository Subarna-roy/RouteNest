# RouteNest — Intelligent Travel Route & Itinerary Planner

## DAA Mini Project

A Python-based travel planning system designed to demonstrate major **Design and Analysis of Algorithms (DAA)** concepts through a practical application.

## Features

1. Search destinations
2. Sort destinations by rating
3. Find the shortest route between cities
4. BFS city traversal
5. DFS city traversal
6. Best attractions within a budget using 0/1 Knapsack
7. Attraction selection using a Greedy approach
8. Generate possible itineraries using Backtracking
9. View algorithm complexity analysis

## DAA Topics Covered

| DAA Topic | Algorithm | Project Use |
|---|---|---|
| Searching | Linear Search | Find destination |
| Searching | Binary Search | Find destination in sorted data |
| Sorting | Bubble Sort | Sort ratings |
| Divide & Conquer | Merge Sort | Sort ratings |
| Divide & Conquer | Quick Sort | Sort ratings |
| Greedy | Greedy Selection | Select attractions within time |
| Dynamic Programming | 0/1 Knapsack | Select attractions within budget |
| Graph | BFS | Explore connected cities |
| Graph | DFS | Explore connected cities |
| Graph | Dijkstra | Shortest travel route |
| Backtracking | Backtracking | Generate itineraries |
| Complexity Analysis | Big-O | Compare algorithms |

## Requirements

- Python 3
- Visual Studio Code
- No external Python packages are required.

## Project Structure

```text
RouteNest/
│
├── main.py
├── places.csv
├── routes.csv
├── README.md
└── sample_output.txt
```

## How to Run in VS Code

### 1. Extract the ZIP

Extract `RouteNest.zip`.

### 2. Open the folder

Open VS Code -> File -> Open Folder -> select:

`RouteNest`

### 3. Open Terminal

VS Code -> Terminal -> New Terminal

### 4. Run

```bash
python main.py
```

If `python` does not work on Windows:

```bash
py main.py
```

## Example

Select:

```text
3. Find shortest route
```

Then enter:

```text
Source: Chandigarh
Destination: Agra
```

The system can find a shortest route such as:

```text
Chandigarh -> Delhi -> Agra
```

## Viva Explanation

### Why is this a DAA project?

The application solves travel planning problems using searching, sorting, greedy, dynamic programming, graph, and backtracking algorithms.

### Why Dijkstra?

Dijkstra finds the shortest path between cities when route distances are non-negative.

### Why Dynamic Programming?

0/1 Knapsack is used to select attractions that give the best total rating while staying within a fixed budget.

### Why Greedy?

The greedy module selects attractions by choosing shorter activities first so that more attractions can fit into the available time.

### Why Backtracking?

Backtracking explores different combinations and removes a choice when it cannot lead to a valid itinerary.

### Why BFS and DFS?

Cities and routes are represented as a graph. BFS and DFS demonstrate graph traversal.

## Complexity Summary

- Linear Search: O(n)
- Binary Search: O(log n)
- Bubble Sort: O(n²)
- Merge Sort: O(n log n)
- Quick Sort: Average O(n log n), Worst O(n²)
- Greedy selection: O(n log n)
- 0/1 Knapsack: O(n × budget)
- BFS: O(V + E)
- DFS: O(V + E)
- Dijkstra (this implementation): O(V²)
- Backtracking: Exponential in the worst case

## Important Note

This is an educational DAA project. It uses a small sample dataset and rule-based algorithms rather than live maps or real-time travel APIs.

## Future Scope

- Add a graphical user interface
- Add real-time map APIs
- Add hotel and transport prices
- Add user preferences
- Add weather information
- Add a larger database
