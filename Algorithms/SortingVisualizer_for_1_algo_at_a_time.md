# Sorting Algorithm Visualizer

This Python script provides a comprehensive visualization of various sorting algorithms using `matplotlib`. It features interactive and animated demonstrations, highlighting every step and operation performed by each algorithm.

## Features

- **Multiple Sorting Algorithms**: Includes Bubble Sort, Insertion Sort, Selection Sort, Merge Sort, Quick Sort, Heap Sort, TimSort, IntroSort, Counting Sort, Radix Sort, Bitonic Sort, Cycle Sort, Sleep Sort, and more!
- **Visual Feedback**: The sorting steps are color-coded for comparisons, swaps, and sorted segments.
- **Configurable Array Generation**: Choose from random, sorted, reversed, nearly sorted, or few unique-value arrays.
- **Interactive Algorithm Selection**: Select the sorting algorithm to visualize through a simple menu.
- **Fun Algorithms**: Includes impractical but fun sorts like BogoSort, BozoSort, SleepSort, and Quantum BogoSort.

---

## Code

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
import math
import sys
import threading
import bisect
from collections import deque

# Generate the array to visualize
def generate_array(size, array_type):
    if array_type == "random":
        return [random.randint(0, size) for _ in range(size)]
    elif array_type == "sorted":
        return list(range(size))
    elif array_type == "reversed":
        return list(range(size, 0, -1))
    elif array_type == "nearly_sorted":
        arr = list(range(size))
        for _ in range(int(size * 0.05)):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif array_type == "few_unique":
        return [random.choice(range(10)) for _ in range(size)]
    else:
        raise ValueError("Unknown array type")

def color_array(length, highlight_indices=[], color="red"):
    colors = ["skyblue"] * length
    for idx in highlight_indices:
        if 0 <= idx < length:
            colors[idx] = color
    return colors

# Bubble Sort (corrected to yield colors)
def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield arr, color_array(n, [j, j+1], "red")
    yield arr, ["green"] * n

# Generator-based sorting algorithms with visual color coding
def insertion_sort(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr, color_array(len(arr), [j + 1, j + 2], "red")
        arr[j + 1] = key
        yield arr, color_array(len(arr), [j + 1], "green")

def selection_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
            yield arr, color_array(n, [i, j, min_idx], "orange")
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr, color_array(n, [i, min_idx], "green")

def gnome_sort(arr):
    arr = arr.copy()
    i = 0
    n = len(arr)
    while i < n:
        if i == 0 or arr[i] >= arr[i - 1]:
            i += 1
        else:
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            yield arr, color_array(n, [i, i-1], "red")
            i -= 1
    yield arr, ["green"] * n

def cocktail_shaker_sort(arr):
    arr = arr.copy()
    n = len(arr)
    start, end = 0, n - 1
    swapped = True
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
            yield arr, color_array(n, [i, i+1], "red")
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
            yield arr, color_array(n, [i, i+1], "red")
        start += 1
    yield arr, ["green"] * n

def comb_sort(arr):
    arr = arr.copy()
    gap = len(arr)
    shrink = 1.3
    sorted_flag = False
    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        i = 0
        while i + gap < len(arr):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False
            yield arr, color_array(len(arr), [i, i+gap], "red")
            i += 1
    yield arr, ["green"] * len(arr)

def merge_sort(arr):
    arr = arr.copy()
    n = len(arr)
    def merge(low, mid, high):
        left = arr[low:mid]
        right = arr[mid:high]
        i = j = 0
        k = low
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
            yield arr, color_array(n, [k], "red")
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            yield arr, color_array(n, [k], "red")
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            yield arr, color_array(n, [k], "red")
    def helper(low, high):
        if high - low <= 1:
            return
        mid = (low + high) // 2
        yield from helper(low, mid)
        yield from helper(mid, high)
        yield from merge(low, mid, high)
    yield from helper(0, n)
    yield arr, ["green"] * n

def quick_sort(arr):
    arr = arr.copy()
    n = len(arr)
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield arr, color_array(n, [i, j], "red")
        arr[i+1], arr[high] = arr[high], arr[i+1]
        yield arr, color_array(n, [i+1, high], "orange")
        return i + 1
    def helper(low, high):
        if low < high:
            pi_gen = partition(low, high)
            while True:
                try:
                    state = next(pi_gen)
                    yield state
                except StopIteration as e:
                    pi = e.value
                    break
            yield from helper(low, pi-1)
            yield from helper(pi+1, high)
    yield from helper(0, n-1)
    yield arr, ["green"] * n

def heap_sort(arr):
    arr = arr.copy()
    n = len(arr)
    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[i] < arr[left]:
            largest = left
        if right < n and arr[largest] < arr[right]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr, color_array(n, [i, largest], "red")
            yield from heapify(n, largest)
    for i in range(n//2 - 1, -1, -1):
        yield from heapify(n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr, color_array(n, [0, i], "orange")
        yield from heapify(i, 0)
    yield arr, ["green"] * n

def shell_sort(arr):
    arr = arr.copy()
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                yield arr, color_array(n, [j, j-gap], "red")
                j -= gap
            arr[j] = temp
            yield arr, color_array(n, [j], "green")
        gap //= 2
    yield arr, ["green"] * n

def tim_sort(arr):
    arr = arr.copy()
    n = len(arr)
    min_run = 32
    def insertion_sort(left, right):
        for i in range(left+1, right+1):
            j = i
            while j > left and arr[j] < arr[j-1]:
                arr[j], arr[j-1] = arr[j-1], arr[j]
                yield arr, color_array(n, [j, j-1], "red")
                j -= 1
    def merge(left, mid, right):
        len1, len2 = mid - left + 1, right - mid
        left_arr = arr[left:mid+1]
        right_arr = arr[mid+1:right+1]
        i = j = 0
        k = left
        while i < len1 and j < len2:
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
            yield arr, color_array(n, [k], "orange")
        while i < len1:
            arr[k] = left_arr[i]
            i += 1
            k += 1
            yield arr, color_array(n, [k], "orange")
        while j < len2:
            arr[k] = right_arr[j]
            j += 1
            k += 1
            yield arr, color_array(n, [k], "orange")
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n-1)
        yield from insertion_sort(start, end)
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n-1, left + size - 1)
            right = min(left + 2*size - 1, n-1)
            if mid < right:
                yield from merge(left, mid, right)
        size *= 2
    yield arr, ["green"] * n

def intro_sort(arr):
    arr = arr.copy()
    n = len(arr)
    max_depth = 2 * math.floor(math.log2(n))
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield arr, color_array(n, [i, j], "red")
        arr[i+1], arr[high] = arr[high], arr[i+1]
        yield arr, color_array(n, [i+1, high], "orange")
        return i + 1
    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[i] < arr[left]:
            largest = left
        if right < n and arr[largest] < arr[right]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr, color_array(n, [i, largest], "red")
            yield from heapify(n, largest)
    def heapsort(start, end):
        nonlocal arr
        n = end - start + 1
        for i in range(n//2 - 1, -1, -1):
            yield from heapify(n, i)
        for i in range(n-1, 0, -1):
            arr[start+i], arr[start] = arr[start], arr[start+i]
            yield arr, color_array(n, [start, start+i], "orange")
            yield from heapify(i, 0)
    def introsort(low, high, depth):
        if high - low < 16:
            for _ in insertion_sort_range(low, high):
                yield _
        elif depth == 0:
            yield from heapsort(low, high)
        else:
            pi_gen = partition(low, high)
            while True:
                try:
                    state = next(pi_gen)
                    yield state
                except StopIteration as e:
                    pi = e.value
                    break
            yield from introsort(low, pi-1, depth-1)
            yield from introsort(pi+1, high, depth-1)
    def insertion_sort_range(left, right):
        for i in range(left+1, right+1):
            j = i
            while j > left and arr[j] < arr[j-1]:
                arr[j], arr[j-1] = arr[j-1], arr[j]
                yield arr, color_array(n, [j, j-1], "red")
                j -= 1
    yield from introsort(0, n-1, max_depth)
    yield arr, ["green"] * n

def cycle_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for cycle_start in range(0, n-1):
        item = arr[cycle_start]
        pos = cycle_start
        for i in range(cycle_start+1, n):
            if arr[i] < item:
                pos += 1
        if pos == cycle_start:
            continue
        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]
        yield arr, color_array(n, [pos], "red")
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start+1, n):
                if arr[i] < item:
                    pos += 1
            while item == arr[pos]:
                pos += 1
            arr[pos], item = item, arr[pos]
            yield arr, color_array(n, [pos], "red")
    yield arr, ["green"] * n

def counting_sort(arr):
    arr = arr.copy()
    n = len(arr)
    k = max(arr) + 1
    count = [0] * k
    output = [0] * n
    for i in range(n):
        count[arr[i]] += 1
        yield arr, color_array(n, [i], "red")
    for i in range(1, k):
        count[i] += count[i-1]
        if i < n:
            yield arr, color_array(n, [i], "orange")
    for i in range(n-1, -1, -1):
        output[count[arr[i]]-1] = arr[i]
        count[arr[i]] -= 1
        yield arr, color_array(n, [i], "red")
    for i in range(n):
        arr[i] = output[i]
        yield arr, color_array(n, [i], "green")
    yield arr, ["green"] * n

def radix_sort(arr):
    arr = arr.copy()
    n = len(arr)
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        output = [0] * n
        count = [0] * 10
        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1
            yield arr, color_array(n, [i], "red")
        for i in range(1, 10):
            count[i] += count[i-1]
            if i < n:
                yield arr, color_array(n, [i], "orange")
        i = n - 1
        while i >= 0:
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1
            yield arr, color_array(n, [i], "red")
        for i in range(n):
            arr[i] = output[i]
            yield arr, color_array(n, [i], "green")
        exp *= 10
    yield arr, ["green"] * n

def bitonic_sort(arr):
    arr = arr.copy()
    n = len(arr)
    def bitonic_merge(low, cnt, direc):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                if direc == (arr[i] > arr[i+k]):
                    arr[i], arr[i+k] = arr[i+k], arr[i]
                    yield arr, color_array(n, [i, i+k], "red")
            yield from bitonic_merge(low, k, direc)
            yield from bitonic_merge(low+k, k, direc)
    def bitonic_sort_helper(low, cnt, direc):
        if cnt > 1:
            k = cnt // 2
            yield from bitonic_sort_helper(low, k, True)
            yield from bitonic_sort_helper(low+k, k, False)
            yield from bitonic_merge(low, cnt, direc)
    yield from bitonic_sort_helper(0, n, True)
    yield arr, ["green"] * n

def bogo_sort(arr):
    arr = arr.copy()
    n = len(arr)
    def is_sorted():
        for i in range(1, n):
            if arr[i-1] > arr[i]:
                return False
        return True
    while not is_sorted():
        random.shuffle(arr)
        yield arr, color_array(n, [], "red")
    yield arr, ["green"] * n

def bozo_sort(arr):
    arr = arr.copy()
    n = len(arr)
    def is_sorted():
        for i in range(1, n):
            if arr[i-1] > arr[i]:
                return False
        return True
    while not is_sorted():
        i = random.randint(0, n-1)
        j = random.randint(0, n-1)
        arr[i], arr[j] = arr[j], arr[i]
        yield arr, color_array(n, [i, j], "red")
    yield arr, ["green"] * n

def sleep_sort(arr):
    arr = arr.copy()
    n = len(arr)
    result = []
    threads = []
    def add_to_result(x):
        time.sleep(x * 0.001)
        result.append(x)
    for x in arr:
        t = threading.Thread(target=add_to_result, args=(x,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    for i in range(n):
        arr[i] = result[i]
        yield arr, color_array(n, list(range(i+1)), "green")
    yield arr, ["green"] * n

def quantum_bogo_sort(arr):
    arr = arr.copy()
    n = len(arr)
    arr.sort()
    yield arr, color_array(n, [], "purple")
    for i in range(5):
        arr_copy = arr.copy()
        random.shuffle(arr_copy)
        yield arr_copy, color_array(n, [], "violet")
    yield arr, ["green"] * n

# Visualizer function
def visualize_sorting(arr, generator_func):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title(f"Sorting Visualization: {generator_func.__name__}")
    bar_rects = ax.bar(range(len(arr)), arr, align="edge", color="skyblue")
    ax.set_xlim(0, len(arr))
    ax.set_ylim(0, int(1.1 * max(arr)) if arr else 0)
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
    iteration = [0]
    start_time = time.time()
    def update_fig(data):
        nonlocal bar_rects
        if isinstance(data, tuple) and len(data) == 2:
            array_state, colors = data
        else:
            array_state = data
            colors = ["skyblue"] * len(arr)
        for rect, height, color in zip(bar_rects, array_state, colors):
            rect.set_height(height)
            rect.set_color(color)
            rect.set_alpha(0.8)
        iteration[0] += 1
        elapsed = time.time() - start_time
        text.set_text(f"Operations: {iteration[0]}\nTime: {elapsed:.2f}s")
        return list(bar_rects) + [text]
    anim = animation.FuncAnimation(
        fig,
        func=update_fig,
        frames=generator_func(arr.copy()),
        interval=1,
        blit=True,
        repeat=False,
        cache_frame_data=False
    )
    plt.tight_layout()
    plt.show()

# Algorithm selection menu
def select_algorithm():
    algorithms = {
        "1": bubble_sort,
        "2": insertion_sort,
        "3": selection_sort,
        "4": gnome_sort,
        "5": cocktail_shaker_sort,
        "6": comb_sort,
        "7": merge_sort,
        "8": quick_sort,
        "9": heap_sort,
        "10": shell_sort,
        "11": tim_sort,
        "12": intro_sort,
        "13": cycle_sort,
        "14": counting_sort,
        "15": radix_sort,
        "16": bitonic_sort,
        "17": bogo_sort,
        "18": bozo_sort,
        "19": sleep_sort,
        "20": quantum_bogo_sort
    }
    print("Available sorting algorithms:")
    print(" 1: Bubble Sort")
    print(" 2: Insertion Sort")
    print(" 3: Selection Sort")
    print(" 4: Gnome Sort")
    print(" 5: Cocktail Shaker Sort")
    print(" 6: Comb Sort")
    print(" 7: Merge Sort")
    print(" 8: Quick Sort")
    print(" 9: Heap Sort")
    print("10: Shell Sort")
    print("11: TimSort")
    print("12: IntroSort")
    print("13: Cycle Sort")
    print("14: Counting Sort")
    print("15: Radix Sort")
    print("16: Bitonic Sort")
    print("17: Bogo Sort (impractical)")
    print("18: Bozo Sort (impractical)")
    print("19: Sleep Sort")
    print("20: Quantum Bogo Sort (joke)")
    choice = input("Select an algorithm (1-20): ")
    return algorithms.get(choice, bubble_sort)

# Example usage
if __name__ == "__main__":
    size = int(input("Enter array size (recommended 50-100): ") or 50)
    array_type = input("Enter array type (random/sorted/reversed/nearly_sorted/few_unique): ") or "random"
    data = generate_array(size, array_type)
    algorithm = select_algorithm()
    visualize_sorting(data, algorithm)
```

---

## How to Use

1. **Install requirements:**
   ```bash
   pip install matplotlib
   ```

2. **Run the script:**
   ```bash
   python your_script_name.py
   ```

3. **Follow the prompts:**
   - Enter array size (recommended: 50-100)
   - Choose the array type (`random`, `sorted`, `reversed`, `nearly_sorted`, `few_unique`)
   - Select the sorting algorithm by entering a number.

4. **Enjoy the visualization!**

---

## Notes

- Some algorithms (BogoSort, BozoSort, SleepSort, Quantum BogoSort) are included for fun and educational purposes and are not practical for large arrays.
- The script uses generator-based implementations to yield at every operation, allowing for step-by-step visualization.
- The color scheme:
  - **Red/Orange**: Elements being compared or swapped.
  - **Green**: Sorted/final state.
  - **Skyblue**: Default state.
  - **Purple/Violet**: Used in Quantum BogoSort for fun.

---

## License

Feel free to use, modify, and share this script for educational and demonstration purposes!