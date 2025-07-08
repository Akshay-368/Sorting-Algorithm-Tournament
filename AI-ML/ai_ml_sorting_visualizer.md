# 📊 AI/ML-Powered Sorting Algorithm Visualizer

## 🧠 Why Use AI/ML in a Sorting Visualizer?

Sorting algorithms are fundamentally deterministic and well-understood. However, their real-world performance varies drastically depending on the **nature of input data**.

This project introduces **Artificial Intelligence (AI) and Machine Learning (ML)** not to perform the sorting itself, but to:

- **Recommend the most efficient algorithm** based on input characteristics.
- **Predict expected performance** (steps, time) before execution.

This transforms a static tool into an **intelligent assistant** that makes informed decisions, guides learners, and supports educators.

---

## 🎯 Features

### 1. Algorithm Recommendation (Classification)

Train a model to recommend the optimal sorting algorithm for a given array profile using features like:

| Feature            | Description                                    |
| ------------------ | ---------------------------------------------- |
| Sortedness         | % of adjacent pairs already in order           |
| Inversions         | % of reversed element pairs                    |
| Unique Ratio       | len(set(arr)) / len(arr)                       |
| Misplaced Elements | How far values are from their correct position |
| Variance           | Spread and standard deviation of values        |

✅ End result: When a user selects an array, the system automatically suggests the best algorithm using a trained ML model.

### 2. Performance Prediction (Regression)

Train another model to predict:

- Estimated Steps 🔄
- Estimated Time ⏱️

✅ End result: Display predictions like:

> *"Expected Steps: 1850 | Time: 1.7s"* before the algorithm even starts.

---

## 🧪 Data Generation Pipeline

To train the models, we simulate **all algorithm matchups** on **all array types**, multiple times:

### Array Types (Terrains)

1. Random
2. Sorted
3. Reversed
4. Nearly Sorted
5. Few Unique Values

### Algorithms (20 total)

- Bubble Sort
- Insertion Sort
- Selection Sort
- Gnome Sort
- Cocktail Shaker Sort
- Comb Sort
- Merge Sort
- Quick Sort
- Heap Sort
- Shell Sort
- TimSort
- IntroSort
- Cycle Sort
- Counting Sort
- Radix Sort
- Bitonic Sort
- Bogo Sort (fun)
- Bozo Sort (fun)
- Sleep Sort
- Quantum Bogo Sort (joke)

### Total Simulation Strategy

- **Each of the 20 algorithms** will be tested **against every other algorithm** (190 unique pairs)
- For **each array type**, each pairing runs **3 times** for statistical reliability.
- That results in: 190 pairs \* 5 array types \* 3 = **2,850 runs**

### Data Recorded Per Run (CSV Dataset)

Each row in the dataset will contain:

| Column           | Description                                 |
| ---------------- | ------------------------------------------- |
| array\_type      | Type of input array                         |
| algorithm\_name  | Name of the algorithm being tested          |
| sortedness       | % of adjacent elements in correct order     |
| inversions       | Number of inversions                        |
| unique\_ratio    | Unique elements / total elements            |
| misplaced\_count | Count of misplaced elements                 |
| variance         | Statistical variance of the data            |
| num\_steps       | Total steps/operations performed            |
| execution\_time  | Time taken (in seconds)                     |
| winner\_against  | Name of algorithm it was compared against   |
| won              | Boolean (1 if this algo was faster, else 0) |
| run\_id          | Unique ID of the test                       |

This data will be stored in a CSV file: `algo_performance_dataset.csv`

---

## 🧠 ML Models Used

### 📌 Classifier (for Best Algorithm Prediction)

- **Input:** Array features
- **Output:** Best-performing algorithm
- **Model:** `DecisionTreeClassifier` or `RandomForestClassifier`

### 📌 Regressor (for Time & Step Prediction)

- **Input:** Array features + algorithm name
- **Output:** Predicted time and steps
- **Model:** `RandomForestRegressor` or `XGBoostRegressor`

---

## 💻 ML Pipeline Code Snippet (Example)

```python
# Example of data extraction for ML
features = extract_features(array)  # sortedness, inversions, variance, etc.
for algo1, algo2 in combinations(all_algorithms, 2):
    for array_type in array_types:
        for _ in range(3):
            array = generate_array(100, array_type)
            t1, steps1 = run_and_time(algo1, array.copy())
            t2, steps2 = run_and_time(algo2, array.copy())

            writer.writerow({
                'array_type': array_type,
                'algorithm_name': algo1.__name__,
                'winner_against': algo2.__name__,
                'won': int(t1 < t2),
                'execution_time': t1,
                'num_steps': steps1,
                **features
            })
```

---

## 🚀 Practical Applications

This project showcases **real-world relevance** in:

### ✅ Educational Tools

- Used by students to understand algorithm behavior dynamically.
- Teachers can demo why some algorithms are better for specific inputs.

### ✅ AI-Augmented Developer Tools

- Could be integrated into code editors/IDEs as a suggestion engine.
- Smart assistants for optimization hints in data pipelines.

### ✅ Resume-Boosting Highlights

This project demonstrates:

- 💡 Understanding of Sorting Algorithms (DSA mastery)
- 🤖 Machine Learning integration (regression + classification)
- 📊 Data Engineering (feature extraction, performance logging)
- 🧰 Software Design (modular architecture, visualization, simulation)
- 💬 Communication (showing insight via predictions and charts)

---

## 📦 Final Thoughts

Even though the sorting is handled by classical algorithms, AI/ML adds:

- Intelligence
- Predictive power
- Automation
- Practical educational value

> **"We don’t use ML to replace sorting – we use it to think smarter about sorting."**

