import os, json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from pathfinder import solve_route
from database import get_db, init_db, close_db

app = Flask(__name__)
CORS(app)
app.teardown_appcontext(close_db)

@app.route('/api/save', methods=['POST'])
def save_layout():
    data = request.json
    db = get_db()
    db.execute('INSERT INTO layouts (grid_data, start_pos, target_pos) VALUES (?, ?, ?)',
               (json.dumps(data['grid']), json.dumps(data['start']), json.dumps(data['targets'])))
    db.commit()
    return jsonify({"status": "saved"})

@app.route('/api/history')
def get_history():
    db = get_db()
    rows = db.execute('SELECT * FROM layouts ORDER BY created_at DESC LIMIT 8').fetchall()
    return jsonify([dict(row) for row in rows])

@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.json
    res = solve_route(data['grid'], data['start'], data['targets'])
    if res is None: return jsonify({"status": "impossible"})
    return jsonify({"total_steps": len(res)-1, "path": res, "targets_collected": len(data['targets'])})

@app.route('/')
def index(): return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('warehouse.sqlite'):
        with app.app_context(): init_db()
    app.run(debug=True, port=5000)
