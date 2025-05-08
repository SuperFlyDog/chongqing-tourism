
---

## 🐜 ACO-SA Route Optimization Web App

This project implements a hybrid route optimization system using **Ant Colony Optimization (ACO)** and **Simulated Annealing (SA)** to solve the **Traveling Salesman Problem (TSP)**. It can find the shortest path that visits multiple locations and displays the optimized route on a web interface. The backend is built with **Flask**, and the frontend is developed using **Vue.js** for interactive visualization.



---

### 📁 Project Structure

```
├── App.vue                  # Main Vue application entry
├── Search.vue               # Component for city input and route query
├── Itinerary.vue            # Component for displaying optimized itinerary
├── app.py                   # Flask backend entry point
├── solve_tsp.py             # Main logic integrating ACO and SA
├── ant_colony.py            # Ant Colony Optimization implementation
├── simulated_annealing.py   # Simulated Annealing implementation
```

---

### ⚙️ Features

* 🧠 **Intelligent Optimization**: Constructs initial solutions using ACO, then refines with SA.
* 🌐 **API Interface**: Accepts coordinates and distance matrix via RESTful API.
* 📈 **Visualization**: Displays city paths before and after optimization.
* 🎯 **Custom Start and End**: Allows setting fixed entrance and exit cities.

---

### 🔧 Installation & Running

#### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

#### 2. Install dependencies

Backend:

```bash
pip install flask flask-cors numpy matplotlib tqdm
```

Frontend (if using Vue CLI):

```bash
npm install
```

#### 3. Run the backend server

```bash
python app.py
```

#### 4. Run the frontend

```bash
npm run serve
```

---

### 🔌 API Endpoint

#### `POST /optimize`

**Request Body:**

```json
{
  "city_coords": [[x1, y1], [x2, y2], ...],
  "distances": [[0, d12, ...], [d21, 0, ...], ...],
  "entrance_index": 0,
  "exit_index": 3
}
```

**Response:**

```json
{
  "optimized_path": [0, 2, 4, 3]
}
```

---

### 🧠 Algorithm Overview

* **Ant Colony Optimization (`ant_colony.py`)**:

  * Uses pheromone trails and heuristics to construct promising routes.
  * Supports custom entrance and exit constraints.
* **Simulated Annealing (`simulated_annealing.py`)**:

  * Refines the ACO output by exploring neighboring permutations.
  * Controlled temperature decay helps escape local optima.
* **Integration (`solve_tsp.py`)**:

  * Combines both algorithms and visualizes results using matplotlib.

---

### 🖼️ Example Output

Running `solve_tsp.py` generates side-by-side plots of ACO and final optimized routes:

<img width="448" alt="image" src="https://github.com/user-attachments/assets/43816b93-8e65-4706-badd-0e600fb9080e" />

Route display on the web page：

<img width="464" alt="image" src="https://github.com/user-attachments/assets/df0acd76-696e-47c1-b55f-433d4ad0f5b6" />


---

### 📄 License

This project is licensed under the MIT License.

---

