So now we’re getting to the **visual core** of our Sorting Tournament project! We'll build a **dynamic visualizer** that animates sorting algorithms in real-time as they manipulate the array.

---

## 🔍 Goals of the Visualization:

1. **Every change** (comparison or swap) made by the algorithm is animated.
2. The array is shown as a **bar chart**, where:

   * Bar **height** represents value.
   * Bar **color** changes during comparisons/swaps.
3. Each algorithm runs **step-by-step**, making it easy to watch how it works.
4. We can plug in **any of the 20 algorithms** one by one.

---

## ✅ Recommended Tools

For my (personal) setup (i7 CPU, 16GB RAM, 6GB VRAM), the best visual library is:

* 🖼️ **`matplotlib` + `FuncAnimation`**

  * Easy to animate updates.
  * Works well in Python projects.
  * No need for GPU-heavy tools like Pygame unless anyone want extra graphics.

---

## 📦 Basic Framework

Here’s a **starter visualizer** that:

* Accepts a sorting function as a generator (which yields steps).
* Animates the sorting process.

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

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

# Bubble Sort as a generator that yields the array after every swap
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr  # Yielding the current state of the array

# Visualizer function
def visualize_sorting(arr, generator_func):
    fig, ax = plt.subplots()
    ax.set_title("Sorting Visualization")

    bar_rects = ax.bar(range(len(arr)), arr, align="edge", color="skyblue")
    ax.set_xlim(0, len(arr))
    ax.set_ylim(0, int(max(arr)) * 1.1)

    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    iteration = [0]

    def update_fig(array, rects, iteration):
        for rect, val in zip(rects, array):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text(f"Operations: {iteration[0]}")

    anim = animation.FuncAnimation(
        fig,
        func=update_fig,
        fargs=(bar_rects, iteration),
        frames=generator_func(arr.copy()),
        interval=1,
        repeat=False,
    )

    plt.show()

# Example usage
if __name__ == "__main__":
    data = generate_array(100, "nearly_sorted")
    visualize_sorting(data, bubble_sort)
```

---

## 🎮 How It Works

* `bubble_sort` is written as a **generator** that `yield`s after every visual-worthy step.
* `visualize_sorting` takes the array and generator, and uses `matplotlib.animation` to update the chart.
* We can plug in any sorting algorithm written as a generator.

---

## 🧩 Next Steps (A note for myself)

1. 🔁 **Convert other algorithms** into generator form.
2. 🎨 Add **color coding** (e.g., red for active comparisons).
3. 🎤 Add **live ML commentary** (text box predictions).
4. 🏆 Automate matchups (one algorithm vs another) and log metrics.
5. 📹 Optionally **save** as video or GIF (great for resume or demo).


