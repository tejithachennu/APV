
import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import sys
import numpy as np

# ======================================================
# SORTING ALGORITHMS (RECURSIVE & ITERATIVE)
# ======================================================

def bubble_sort_steps(arr):
    a, n, steps = arr.copy(), len(arr), []
    comparisons = swaps = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            steps.append({
                "array": a.copy(), "i": i, "j1": j, "j2": j + 1, "sorted_start": n - i,
                "comparisons": comparisons, "swaps": swaps,
                "condition": f"A[j] > A[j+1] \Rightarrow {a[j]} > {a[j+1]}",
                "explanation": f"Comparing index {j} and {j+1}."
            })
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                steps.append({
                    "array": a.copy(), "i": i, "j1": j, "j2": j + 1, "sorted_start": n - i,
                    "comparisons": comparisons, "swaps": swaps,
                    "condition": r"\text{Swap Required}",
                    "explanation": f"Swapping {a[j+1]} and {a[j]}."
                })
    return steps

def selection_sort_steps(arr):
    a, n, steps = arr.copy(), len(arr), []
    comparisons = swaps = 0
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            steps.append({
                "array": a.copy(), "i": i, "j1": j, "j2": min_idx, "sorted_start": i,
                "comparisons": comparisons, "swaps": swaps,
                "condition": f"A[j] < A[min\_idx] \Rightarrow {a[j]} < {a[min_idx]}",
                "explanation": f"Searching for new minimum. Current min is index {min_idx}."
            })
            if a[j] < a[min_idx]: min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
        swaps += 1
        steps.append({
            "array": a.copy(), "i": i, "j1": i, "j2": min_idx, "sorted_start": i + 1,
            "comparisons": comparisons, "swaps": swaps,
            "condition": r"\text{Placing Minimum}",
            "explanation": f"Placing the smallest found element at index {i}."
        })
    return steps

def insertion_sort_steps(arr):
    a, n, steps = arr.copy(), len(arr), []
    comparisons = swaps = 0
    for i in range(1, n):
        key, j = a[i], i - 1
        while j >= 0:
            comparisons += 1
            steps.append({
                "array": a.copy(), "i": i, "j1": j, "j2": j + 1, "sorted_start": i,
                "comparisons": comparisons, "swaps": swaps,
                "condition": f"key < A[j] \Rightarrow {key} < {a[j]}",
                "explanation": f"Checking if {key} should move left of index {j}."
            })
            if a[j] > key:
                a[j + 1] = a[j]
                j -= 1
                swaps += 1
            else: break
        a[j + 1] = key
        steps.append({
            "array": a.copy(), "i": i, "j1": j + 1, "j2": -1, "sorted_start": i + 1,
            "comparisons": comparisons, "swaps": swaps,
            "condition": r"\text{Key Inserted}",
            "explanation": f"Inserted key into its final sorted position."
        })
    return steps

def quick_sort_steps(arr):
    a, steps = arr.copy(), []
    stats = {"comp": 0, "swaps": 0}

    def partition(low, high):
        pivot = a[high]
        i = low - 1
        for j in range(low, high):
            stats["comp"] += 1
            steps.append({
                "array": a.copy(), "i": low, "j1": j, "j2": high, "sorted_start": -1,
                "comparisons": stats["comp"], "swaps": stats["swaps"],
                "condition": f"A[j] < pivot \Rightarrow {a[j]} < {pivot}",
                "explanation": f"Comparing element with pivot at index {high}."
            })
            if a[j] < pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                stats["swaps"] += 1
        a[i + 1], a[high] = a[high], a[i + 1]
        stats["swaps"] += 1
        steps.append({
            "array": a.copy(), "i": low, "j1": i + 1, "j2": high, "sorted_start": -1,
            "comparisons": stats["comp"], "swaps": stats["swaps"],
            "condition": r"\text{Pivot Positioned}",
            "explanation": f"Partitioning done. Pivot moved to index {i+1}."
        })
        return i + 1

    def recursive_qsort(low, high):
        if low < high:
            p = partition(low, high)
            recursive_qsort(low, p - 1)
            recursive_qsort(p + 1, high)

    recursive_qsort(0, len(a) - 1)
    return steps

def merge_sort_steps(arr):
    a, steps = arr.copy(), []
    stats = {"comp": 0, "swaps": 0}

    def merge(low, mid, high):
        L, R = a[low:mid+1], a[mid+1:high+1]
        i = j = 0
        k = low
        while i < len(L) and j < len(R):
            stats["comp"] += 1
            steps.append({
                "array": a.copy(), "i": low, "j1": low + i, "j2": mid + 1 + j, "sorted_start": -1,
                "comparisons": stats["comp"], "swaps": stats["swaps"],
                "condition": f"L[i] \leq R[j] \Rightarrow {L[i]} \leq {R[j]}",
                "explanation": "Comparing elements from split subarrays."
            })
            if L[i] <= R[j]:
                a[k] = L[i]; i += 1
            else:
                a[k] = R[j]; j += 1; stats["swaps"] += 1
            k += 1
        while i < len(L): a[k] = L[i]; i += 1; k += 1
        while j < len(R): a[k] = R[j]; j += 1; k += 1
        steps.append({
            "array": a.copy(), "i": low, "j1": low, "j2": high, "sorted_start": -1,
            "comparisons": stats["comp"], "swaps": stats["swaps"],
            "condition": r"\text{Merge Complete}",
            "explanation": f"Subarray merged from index {low} to {high}."
        })

    def recursive_msort(low, high):
        if low < high:
            mid = (low + high) // 2
            recursive_msort(low, mid)
            recursive_msort(mid + 1, high)
            merge(low, mid, high)

    recursive_msort(0, len(a) - 1)
    return steps

# ======================================================
# PERFORMANCE & VISUALIZATION 
# ======================================================

def run_benchmarks(algo_name):
    st.sidebar.markdown("### 🧬 Performance Mapping")
    sizes = [10, 30, 60, 100]
    times, ops, memory = [], [], []
    for n in sizes:
        test_data = [random.randint(1, 1000) for _ in range(n)]
        memory.append(sys.getsizeof(test_data) + (n * sys.getsizeof(int())))
        start = time.perf_counter()
        if algo_name == "Bubble Sort": res = bubble_sort_steps(test_data)
        elif algo_name == "Selection Sort": res = selection_sort_steps(test_data)
        elif algo_name == "Insertion Sort": res = insertion_sort_steps(test_data)
        elif algo_name == "Quick Sort": res = quick_sort_steps(test_data)
        else: res = merge_sort_steps(test_data)
        times.append(time.perf_counter() - start)
        ops.append(res[-1]["comparisons"] + res[-1]["swaps"])
    fig, ax1 = plt.subplots(figsize=(5, 3))
    ax1.set_xlabel('n'); ax1.set_ylabel('Time', color='red'); ax1.plot(sizes, times, 'ro-')
    ax2 = ax1.twinx(); ax2.set_ylabel('Ops', color='blue'); ax2.plot(sizes, ops, 'bx--')
    st.sidebar.pyplot(fig)
    st.sidebar.write(f"**Max Memory:** {max(memory)} bytes")

def render_array_boxes(arr, j1, j2, sorted_start, algo_name):
    cols = st.columns(len(arr))
    for idx, val in enumerate(arr):
        color = "#ADD8E6"
        if algo_name == "Bubble Sort" and idx >= sorted_start: color = "#90EE90"
        elif (algo_name in ["Selection Sort", "Insertion Sort"]) and idx < sorted_start: color = "#90EE90"
        if idx == j1 or idx == j2: color = "#FF7F7F"
        with cols[idx]:
            st.markdown(f'<div style="padding:14px; text-align:center; border-radius:8px; background-color:{color}; font-size:20px; font-weight:bold; border: 1px solid #555;">{val}</div><p style="text-align:center;font-size:12px;color:grey;">idx {idx}</p>', unsafe_allow_html=True)

# ======================================================
# STREAMLIT UI & STATE MANAGEMENT
# ======================================================

st.set_page_config(page_title="Algorithm Visualizer Pro", layout="wide")
st.title("📊 Multi-Algorithm Visualizer")
st.markdown("---")

if 'current_step_idx' not in st.session_state: st.session_state.current_step_idx = 0
if 'is_playing' not in st.session_state: st.session_state.is_playing = False

st.sidebar.header("⚙️ Configuration")
algo_choice = st.sidebar.selectbox("Select Algorithm", ["Bubble Sort", "Selection Sort", "Insertion Sort", "Quick Sort", "Merge Sort"])
visual_mode = st.sidebar.radio("Visualization Style", ["Array Boxes", "Bar Graph"])
input_mode = st.sidebar.radio("Input Source", ["Automatic (Random)", "Manual (User Input)"])
speed = st.sidebar.slider("Step Delay (seconds)", 0.05, 2.0, 0.4)

if st.sidebar.checkbox("Show Performance Analysis"):
    run_benchmarks(algo_choice)

if input_mode == "Manual (User Input)":
    user_input = st.text_input("Numbers (comma-separated):")
    try:
        data = [int(x.strip()) for x in user_input.split(",") if x.strip()]
        if len(data) < 2: st.stop()
    except: st.error("Invalid input."); st.stop()
else:
    n = st.sidebar.slider("Array Size (n)", 5, 15, 8)
    if 'random_data' not in st.session_state or len(st.session_state.random_data) != n:
        st.session_state.random_data = random.sample(range(5, 100), n)
        st.session_state.current_step_idx = 0
    data = st.session_state.random_data

complexities = {
    "Bubble Sort": {"time": "O(n^2)", "space": "O(1)"},
    "Selection Sort": {"time": "O(n^2)", "space": "O(1)"},
    "Insertion Sort": {"time": "O(n^2)", "space": "O(1)"},
    "Quick Sort": {"time": "O(n \log n)", "space": "O(\log n)"},
    "Merge Sort": {"time": "O(n \log n)", "space": "O(n)"}
}
comp_data = complexities[algo_choice]

# Initial Step Calculation
if algo_choice == "Bubble Sort": steps = bubble_sort_steps(data)
elif algo_choice == "Selection Sort": steps = selection_sort_steps(data)
elif algo_choice == "Insertion Sort": steps = insertion_sort_steps(data)
elif algo_choice == "Quick Sort": steps = quick_sort_steps(data)
else: steps = merge_sort_steps(data)

# Control Buttons (Row 1)
col_b1, col_b2, col_b3 = st.columns([1, 1, 8])
with col_b1:
    if st.session_state.is_playing:
        if st.button("⏸ Pause"): st.session_state.is_playing = False; st.rerun()
    else:
        if st.button("▶ Play/Resume"): st.session_state.is_playing = True; st.rerun()
with col_b2:
    if st.button("🔄 Reset"):
        st.session_state.current_step_idx = 0; st.session_state.is_playing = False
        if input_mode == "Automatic (Random)": st.session_state.random_data = random.sample(range(5, 100), n)
        st.rerun()

st.subheader(f"Current Execution: {algo_choice}")
visual_placeholder = st.empty()
col_math, col_stats = st.columns([2, 1])
with col_math: math_placeholder = st.empty()
with col_stats: stats_placeholder = st.empty()

# ======================================================
# ANIMATION LOOP (BLINK-FREE)
# ======================================================

# Static display for when paused or at the start
if st.session_state.current_step_idx < len(steps):
    step = steps[st.session_state.current_step_idx]
    with visual_placeholder.container():
        render_array_boxes(step["array"], step["j1"], step["j2"], step["sorted_start"], algo_choice)
    math_placeholder.markdown(f"### 📐 Step Logic\n**Index/Pivot:** `{step['i']}` | **Predicate:** ${step['condition']}$\n> {step['explanation']}")
    stats_placeholder.markdown(f"### 📊 Live Metrics\n| Metric | Value |\n| :--- | :--- |\n| Comparisons | **{step['comparisons']}** |\n| Swaps/Ops | **{step['swaps']}** |\n| Time | **{comp_data['time']}** |\n| Space | **{comp_data['space']}** |")

# Active Play Loop
if st.session_state.is_playing:
    while st.session_state.current_step_idx < len(steps):
        if not st.session_state.is_playing:
            break
        
        step = steps[st.session_state.current_step_idx]
        with visual_placeholder.container():
            render_array_boxes(step["array"], step["j1"], step["j2"], step["sorted_start"], algo_choice)
        
        math_placeholder.markdown(f"### 📐 Step Logic\n**Index/Pivot:** `{step['i']}` | **Predicate:** ${step['condition']}$\n> {step['explanation']}")
        stats_placeholder.markdown(f"### 📊 Live Metrics\n| Metric | Value |\n| :--- | :--- |\n| Comparisons | **{step['comparisons']}** |\n| Swaps/Ops | **{step['swaps']}** |\n| Time | **{comp_data['time']}** |\n| Space | **{comp_data['space']}** |")
        
        st.session_state.current_step_idx += 1
        time.sleep(speed)
        
        if st.session_state.current_step_idx >= len(steps):
            st.session_state.is_playing = False
            st.success("Sorting Sequence Terminated Successfully!")
            st.balloons()
            st.rerun()