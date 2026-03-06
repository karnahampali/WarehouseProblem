# RouteMaster Pro | Intelligent Warehouse Logistics

RouteMaster Pro is a high-performance warehouse pathfinding application designed for the 2026 Hackarena. It utilizes a **Breadth-First Search (BFS)** algorithm to calculate the most efficient route for pickers while handling dynamic obstacles and providing high-fidelity visual datasheets.

---

## 🚀 Features

* **Dynamic Pathfinding**: Utilizes BFS to guarantee the shortest path between start and target.
* **Impossible Path Detection**: Automatically identifies and alerts users when a target is completely walled off.
* **Persistent Storage**: Integrated **SQLite** database to save, view, and reload previous warehouse layouts.
* **Datasheet Export**: Generate high-resolution JPG exports of the warehouse grid, including the visual route trail and mandatory JSON statistics.
* **Supabase Authentication**: Secure user access and session management.

---

## 🛠️ Tech Stack

* **Backend**: Python (Flask)
* **Database**: SQLite3
* **Frontend**: HTML5, Tailwind CSS, JavaScript
* **Libraries**: html2canvas (for JPG export), Supabase JS

---

## 📋 Installation & Setup

1. **Clone the repository**:
```bash
git clone <https://github.com/karnahampali/WarehouseProblem>
cd routemaster

```


2. **Install dependencies**:
```bash
pip install -r requirements.txt

```


3. **Configure Environment**:
Create a `.env` file in the root directory and add your Supabase credentials:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key

```


4. **Initialize Database & Run**:
```bash
python app.py

```


The application will automatically initialize the SQLite database on the first run.

---

## 📊 Mandatory JSON Schema

Every successful route execution generates a schema including:

* `timestamp`: Execution time.
* `total_steps`: Number of moves taken.
* `packages_collected`: Verification of target reaching.
* `path`: Array of `[row, col]` coordinates.
