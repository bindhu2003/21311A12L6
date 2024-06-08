from flask import Flask, request, jsonify
import requests
import time
from collections import deque

app = Flask(__name__)

WINDOW_SIZE = 10
numbers_queue = deque(maxlen=WINDOW_SIZE)

def fetch_numbers():
    response = requests.get("http://localhost:3000/")
    if response.status_code == 200:
        return response.json()["numbers"]
    else:
        return []

def calculate_average():
    if len(numbers_queue) == 0:
        return 0
    return sum(numbers_queue) / len(numbers_queue)

@app.route("/numbers", methods=["POST"])
def receive_numbers():
    data = request.json
    qualified_ids = data.get("qualified_ids", [])
    fetched_numbers = []

    for qualified_id in qualified_ids:
        if qualified_id == "p":
            fetched_numbers.extend(fetch_prime_numbers())
        elif qualified_id == "e":
            fetched_numbers.extend(fetch_even_numbers())
        elif qualified_id == "f":
            fetched_numbers.extend(fetch_fibonacci_numbers())
        elif qualified_id == "r":
            fetched_numbers.extend(fetch_random_numbers())

    unique_numbers = set(fetched_numbers)
    unique_numbers.difference_update(set(numbers_queue))

    numbers_queue.extend(unique_numbers)

    if len(numbers_queue) >= WINDOW_SIZE:
        average = calculate_average()
        numbers_before = list(numbers_queue)[:WINDOW_SIZE]
        numbers_queue.pop(0)
        numbers_after = list(numbers_queue)[:WINDOW_SIZE]
        return jsonify({
            "windowPrevState": numbers_before,
            "windowCurrState": numbers_after,
            "average": average
        })

    return "Numbers received and stored successfully", 200

@app.route("/state", methods=["GET"])
def get_current_state():
    return jsonify({
        "windowCurrState": list(numbers_queue),
        "average": calculate_average()
    })

if __name__ == "__main__":
    app.run(host="localhost", port=9876)
