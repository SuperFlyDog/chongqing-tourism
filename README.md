
```markdown
# Chongqing Tourism Path Optimization Web App

This project is a full-stack web application designed to optimize travel routes for tourists visiting Chongqing. It integrates a **Vue.js** frontend with a **Flask** backend that uses **Ant Colony Optimization (ACO)** and **Simulated Annealing (SA)** algorithms to solve the **Traveling Salesman Problem (TSP)**.

## 📌 Features

- 🧭 Route optimization using ACO + SA metaheuristics
- 🧠 Intelligent path planning with entrance and exit constraints
- 🖥️ Interactive front-end built with Vue.js
- 🔙 Backend API built with Flask
- 📊 Visual display of optimized paths

## 🗂️ Project Structure

```

chongqing-tourism/
├── frontend/                  # Vue.js components (App.vue, Search.vue, Itinerary.vue, etc.)
├── backend/                   # Flask API
│   ├── app.py                 # Flask API entry
│   ├── solve\_tsp.py           # Core logic combining ACO & SA
│   ├── ant\_colony.py          # Ant Colony Optimization implementation
│   └── simulated\_annealing.py # Simulated Annealing implementation

````

## 🚀 How to Run

### Frontend (Vue.js)

```bash
cd frontend
npm install
npm run serve
````

### Backend (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Sample API Usage

POST to `/optimize` with JSON body:

```json
{
  "city_coords": [[0,0], [1,1], [2,2], ...],
  "distances": [[0, 1.4, 2.0, ...], ...],
  "entrance_index": 0,
  "exit_index": 5
}
```

Returns:

```json
{
  "optimized_path": [0, 3, 2, 4, 5]
}
```

## 🔧 Algorithms Used

* **Ant Colony Optimization (ACO)** for initial solution generation
* **Simulated Annealing (SA)** for local refinement
* Supports entrance/exit constraints and dynamic distance matrices

## 📷 Screenshots

(Insert demo GIFs or screenshots of your app UI here)

## 📄 License

MIT License
