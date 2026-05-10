# Project Documentation: CISC vs RISC Architecture Simulator

## 1. Project Overview

This project is an interactive dashboard built with Python and Streamlit. It visually demonstrates the fundamental differences between Complex Instruction Set Computers (CISC, e.g., x86) and Reduced Instruction Set Computers (RISC, e.g., MIPS/ARM).

The application features custom-built software simulators that parse and execute assembly language line-by-line, tracking cycle counts, instruction counts, register states, and memory allocations to prove how different CPU architectures handle the exact same logical tasks.

---

## 2. Codebase Architecture (Separation of Concerns)

The project is divided into four distinct files to separate the backend logic from the frontend UI. This makes the code highly modular, readable, and easy to maintain.

### **File Structure**

* `simulators.py` — The "CPU Hardware" (Backend Logic)
* `data.py` — The "Database" (Static Data & Assets)
* `ui_utils.py` — The "Graphics Engine" (Charts & CSS)
* `app.py` — The "Dashboard" (Main Streamlit UI)

### How to run

Use requirements.txt to install these:
- Streamlit
- Plotly
- Pandas

---

## 3. Detailed File Breakdown & Working Mechanics

### A. `simulators.py` (The Core Engine)

This file contains the actual CPU simulation logic. It defines two classes, `CISC` and `RISC`, which act as virtual processors.

**How the CISC Class Works:**

* **Memory Direct Access:** CISC allows arithmetic operations to fetch data directly from memory. The custom `_get()` method parses operands to see if they are surrounded by brackets (e.g., `[100]`). If so, it fetches from the simulated RAM dictionary (`self.M`); otherwise, it fetches from the Register dictionary (`self.R`).
* **Variable Cycle Costs:** The `CYCLE_COST` dictionary assigns different weights to instructions. A simple `INC` takes 1 cycle, but an `IMUL` (multiply) takes 4 cycles.
* **Execution:** The `run()` method reads the assembly string line-by-line. It splits the instruction (opcode) from its operands, performs the math, updates the simulated hardware state, and appends a formatted string to the execution `log`.

**How the RISC Class Works:**

* **Load/Store Architecture:** RISC math operations (`ADD`, `MUL`, etc.) are strictly forbidden from touching memory. The code enforces this by having a simpler `_reg()` helper that *only* looks at the register file.
* **Memory Isolation:** The only instructions allowed to interact with the simulated RAM (`self.M`) are explicitly `LOAD` and `STORE`.
* **Uniform Cycle Costs:** Almost all instructions cost exactly 1 clock cycle, mirroring how real RISC processors are heavily pipelined and optimized.

### B. `data.py` (The Data Layer)

This file stores all the static dictionaries and lists. Keeping this separated ensures the main UI file isn't cluttered with raw data.

* **`PRESETS`:** A dictionary containing pairs of assembly code. For every logical task (like adding two numbers), it stores a CISC version and a RISC version. This fuels the dropdown menu in the simulator.
* **Benchmarking Datasets:** Dictionaries like `SPEC_DATA`, `TRANSISTOR_DATA`, and `PIPE_DATA` hold real-world historical data regarding CPU performance, Moore's Law, and pipeline depths.

### C. `ui_utils.py` (The Presentation Layer)

This file handles complex visual rendering that would otherwise make the Streamlit file messy.

* **`CUSTOM_CSS`:** Injects custom styling, fonts, and colors to make the Streamlit app look like a modern, dark-mode technical dashboard.
* **`bar_chart()`:** A wrapper function for the `plotly.graph_objects` library. It standardizes the colors and spacing so every chart looks consistent.
* **`pipeline_html()`:** A custom HTML/CSS Grid generator. It uses a mathematical offset (`cycle = i + j`) to dynamically generate the diagonal "staircase" visual of a superscalar CPU pipeline based on user input.

### D. `app.py` (The Main Application)

This is the entry point for Streamlit. It imports the components from the other three files and wires them together.

* **Routing:** It handles the four-tab layout (Concepts, Simulator, Pipeline, Benchmarks).
* **State Management:** It captures user inputs (like clicking the "Execute Both" button or moving the Pipeline slider).
* **Data Binding:** When the user clicks "Execute", `app.py` takes the text from the UI, passes it into `CISC().run()` and `RISC().run()` from `simulators.py`, receives the resulting data (cycles, logs, register states), and passes that data into Streamlit metric widgets and Plotly charts to display to the user.

---

## 4. The Execution Flow (How a simulation runs)

1. **User Input:** The user selects "A × B (multiply)" from the dropdown in `app.py`.
2. **Data Fetch:** `app.py` retrieves the corresponding assembly strings from `PRESETS` in `data.py` and populates the text boxes.
3. **Trigger:** The user clicks "Execute Both".
4. **Simulation:** * `app.py` passes the CISC text to `simulators.CISC.run()`.
* The backend loops through the text. It sees `MOV EAX, [100]`. It updates the virtual `EAX` register with the value inside the virtual memory address `100`. It adds 2 cycles to the counter.
* It repeats this for the RISC text.


5. **Render:** The simulator returns the final total cycles, instructions, memory states, and execution logs. `app.py` formats these into Pandas DataFrames and renders them to the screen.