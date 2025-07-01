
# 🏟️ Battle Arena Configuration for Sorting Tournament

the algorithms are ready, and now it’s time to design the **battle arenas** they’ll compete in — i.e., the **input array types and sizes**.



* Size range: **5,000 to 12,000 elements**
* Types: **Partially sorted**, **random**, and **reversed**

Let’s finalize the dataset design in a structured way for consistency, variety, and fairness across all matches. 👇

---

## 🧪 1. **Array Sizes to Use**

Picking up a few representative sizes across the range to simulate small to moderately large stress.

| Size Label | Actual Size | Notes                                       |
| ---------- | ----------- | ------------------------------------------- |
| Small      | 5,000       | Good for visual comparisons                 |
| Medium     | 8,000       | Mid-range challenge                         |
| Large      | 12,000      | Pushes slow sorts, real test for meme algos |

ALso  randomly pick sizes between 5k–12k during matches, for variety.

✅ Possible Implemenation: **Use 3–5 unique sizes**, either fixed or randomly sampled.

---

## 🎭 2. **Array Types to Compete On**

Here are the final 5 **data condition categories**:

| Array Type        | Description                                            |
| ----------------- | ------------------------------------------------------ |
| **Random**        | Fully randomized integers                              |
| **Reversed**      | Descending order                                       |
| **Sorted**        | Already sorted (ascending)                             |
| **Nearly Sorted** | 90–95% sorted, rest shuffled                           |
| **Few Unique**    | Mostly repeated elements (e.g., only 10 unique values) |

✅ Including **"Few Unique"** is for testing linear sorts like **Counting Sort** and **Radix Sort**.

---

## 🧪 3. **How to Generate Them (Python)**

```python
import random

def generate_array(size, array_type):
    if array_type == "random":
        return [random.randint(0, size) for _ in range(size)]
    elif array_type == "sorted":
        return list(range(size))
    elif array_type == "reversed":
        return list(range(size, 0, -1))
    elif array_type == "nearly_sorted":
        arr = list(range(size))
        for _ in range(int(size * 0.05)):  # Shuffle 5% of the array
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif array_type == "few_unique":
        return [random.choice(range(10)) for _ in range(size)]
    else:
        raise ValueError("Unknown array type")
```

---

## 🎯 Matchup Format Strategy

Each algorithm:

* Faces **every other algorithm**
* On **each array type**
* At **each array size**
* **5 rounds each** to average out randomness

This gives a rich, balanced, and diverse data for ML and analysis later.

---

## 🧠 Summary of Battle Arena Configuration

| Feature          | Options                                             |
| ---------------- | --------------------------------------------------- |
| Sizes            | 5,000 – 12,000 (e.g., 5k, 8k, 12k)                  |
| Types            | Random, Reversed, Sorted, Nearly Sorted, Few Unique |
| Rounds per Match | 5 (averaged)                                        |

---


