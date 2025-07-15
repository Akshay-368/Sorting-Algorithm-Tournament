import random
import time
import csv
import sys
import os
from collections import defaultdict

# =============================================
# ML DATASET GENERATION MODULE
# =============================================

# Define algorithm groups for appropriate sizing
ALGO_GROUP = {
    bogo_sort: 5,
    bozo_sort: 5,
    quantum_bogo_sort: 5,
    sleep_sort: 100,
}

# Default size for algorithms not in ALGO_GROUP
DEFAULT_SIZE = 100

# List of all algorithms
ALGORITHMS = [
    bubble_sort, insertion_sort, selection_sort, gnome_sort, cocktail_shaker_sort,
    comb_sort, merge_sort, quick_sort, heap_sort, shell_sort, tim_sort, intro_sort,
    cycle_sort, counting_sort, radix_sort, bitonic_sort, bogo_sort, bozo_sort,
    sleep_sort, quantum_bogo_sort
]

# Array types for testing
ARRAY_TYPES = ["random", "sorted", "reversed", "nearly_sorted", "few_unique"]

def compute_features(arr):
    """Compute features for the input array."""
    n = len(arr)
    sorted_arr = sorted(arr)
    
    # 1. Sortedness (% of adjacent pairs in order)
    sorted_pairs = 0
    if n > 1:
        for i in range(n-1):
            if arr[i] <= arr[i+1]:
                sorted_pairs += 1
        sortedness = (sorted_pairs / (n-1)) * 100
    else:
        sortedness = 100.0
    
    # 2. Inversions (count of inverted pairs)
    inversions = 0
    for i in range(n):
        for j in range(i+1, n):
            if arr[i] > arr[j]:
                inversions += 1
                
    # 3. Unique Ratio
    unique_ratio = len(set(arr)) / n if n > 0 else 1.0
    
    # 4. Misplaced Elements
    misplaced = sum(1 for i in range(n) if arr[i] != sorted_arr[i])
    
    # 5. Variance
    if n > 0:
        mean = sum(arr) / n
        variance = sum((x - mean) ** 2 for x in arr) / n
    else:
        variance = 0.0
        
    return sortedness, inversions, unique_ratio, misplaced, variance

def run_algorithm(algorithm, arr):
    """Run algorithm and return steps/time."""
    arr_copy = arr.copy()
    gen = algorithm(arr_copy)
    steps = 0
    start_time = time.time()
    
    try:
        while True:
            next(gen)
            steps += 1
    except StopIteration:
        elapsed = time.time() - start_time
        return steps, elapsed
    except Exception as e:
        print(f"Error running {algorithm.__name__}: {str(e)}")
        return float('inf'), float('inf')

def generate_dataset(filename="algo_performance_dataset.csv"):
    """Generate ML dataset and save to CSV."""
    # Create all unique algorithm pairs
    pairs = []
    for i in range(len(ALGORITHMS)):
        for j in range(i+1, len(ALGORITHMS)):
            pairs.append((ALGORITHMS[i], ALGORITHMS[j]))
    
    run_id = 0
    total_runs = len(pairs) * len(ARRAY_TYPES) * 3
    completed = 0
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "array_type", "algorithm_name", "sortedness", "inversions", 
            "unique_ratio", "misplaced_count", "variance", "num_steps",
            "execution_time", "winner_against", "won", "run_id"
        ])
        
        for array_type in ARRAY_TYPES:
            for algo1, algo2 in pairs:
                # Determine appropriate array size
                size1 = ALGO_GROUP.get(algo1, DEFAULT_SIZE)
                size2 = ALGO_GROUP.get(algo2, DEFAULT_SIZE)
                size = min(size1, size2)
                
                for iteration in range(3):
                    run_id += 1
                    completed += 1
                    arr = generate_array(size, array_type)
                    
                    # Compute features (using unsorted array)
                    features = compute_features(arr)
                    
                    # Run both algorithms
                    steps1, time1 = run_algorithm(algo1, arr)
                    steps2, time2 = run_algorithm(algo2, arr)
                    
                    # Determine winner (based on execution time)
                    won1 = 1 if time1 < time2 else 0
                    won2 = 1 if time2 < time1 else 0
                    
                    # Write results for algorithm 1
                    writer.writerow([
                        array_type, algo1.__name__, features[0], features[1],
                        features[2], features[3], features[4], steps1,
                        time1, algo2.__name__, won1, run_id
                    ])
                    
                    # Write results for algorithm 2
                    writer.writerow([
                        array_type, algo2.__name__, features[0], features[1],
                        features[2], features[3], features[4], steps2,
                        time2, algo1.__name__, won2, run_id
                    ])
                    
                    # Progress tracking
                    progress = (completed / total_runs) * 100
                    print(f"Progress: {progress:.1f}% | "
                        f"Run {run_id}: {algo1.__name__} vs {algo2.__name__} "
                        f"on {array_type} array")
    
    print(f"Dataset generated successfully: {filename}")

# =============================================
# INTEGRATION WITH EXISTING CODE
# =============================================

if __name__ == "__main__":
        print("Starting ML dataset generation...")
        generate_dataset()
        print("Dataset generation completed!")
    
